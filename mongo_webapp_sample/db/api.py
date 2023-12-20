import logging

import pymongo

from mongo_webapp_sample import conf
from mongo_webapp_sample import exception
from mongo_webapp_sample import utils

LOG = logging.getLogger('mongo_webapp_sample')


def convert_mongo_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except pymongo.errors.DuplicateKeyError as ex:
            LOG.debug(ex)
            raise exception.Conflict()

    return wrapper


class DatabaseAPI:
    def __init__(self):
        self._cfg = conf.get_cfg()
        self._client = pymongo.MongoClient(
            str(self._cfg.mongo_url),
            connectTimeoutMS=(1000 * self._cfg.mongo_conn_timeout),
            serverSelectionTimeoutMS=(1000 * self._cfg.mongo_conn_timeout),
            timeoutMS=(1000 * self._cfg.mongo_op_timeout)
        )
        self._db = self._client[self._cfg.mongo_db_name]

    def initialize_indexes(self):
        self._stores.create_index("name", unique=True)
        # enable text search against the following fields
        self._stores.create_index({
            "name": "text",
            "description": "text",
            "tags": "text",
        })
        # geospatial index
        self._stores.create_index({"location": "2dsphere"})

    def ping(self):
        self._client.admin.command('ping')

    def delete_database(self):
        # Used by the functional tests to clean up temporary databases.
        self._client.drop_database(self._cfg.mongo_db_name)

    def delete_collection(self, name, keep_indexes=True):
        # Used by the functional tests to clean up temporary collections.
        if keep_indexes:
            self._db[name].delete_many({})
        else:
            self._client.drop_collection(name)

    @property
    def _stores(self):
        # For convenience, we're defining a property that accesses
        # the "stores" collection. This also prevents us from accessing
        # the wrong collection due to typos.
        return self._db['stores']

    @convert_mongo_errors
    def add_store(self, store):
        utils.ensure_id(store)
        utils.ensure_location_type(store)

        result = self._stores.insert_one(store)
        created_store = self._stores.find_one(
            {"_id": result.inserted_id})
        return created_store

    @convert_mongo_errors
    def get_store(self, store_id):
        return self._stores.find_one({'_id': store_id})

    @convert_mongo_errors
    def delete_store(self, store_id):
        self._stores.delete_one({'_id': store_id})

    @convert_mongo_errors
    def update_store(self, store_id, updates):
        utils.ensure_location_type(updates)
        self._stores.find_one_and_update(
            {'_id': store_id},
            {'$set': updates})
        return self.get_store(store_id)

    @convert_mongo_errors
    def list_stores(self, filters):
        # TODO: pagination would be nice to have. For now, we'll
        # use a hard limit.
        mongo_filter = {}
        unrecognized_filters = {}

        # We'll process the input filter, generating a MongoDB
        # expression.
        for key, value in filters.items():
            # Collection fields that can be used without any
            # further processing.
            unprocessed_fields = ['name', 'description']
            if key in unprocessed_fields:
                mongo_filter[key] = value
            elif key == 'text':
                # perform text search
                mongo_filter['$text'] = {'$search': value}
            elif key == 'near':
                # Geospatial search
                try:
                    lon, lat = map(float, value.split(','))
                except ValueError:
                    msg = (
                        "Invalid 'near' filter: %s. Expecting two comma "
                        "separated numeric values " % value)
                    raise exception.Invalid(msg)

                mongo_filter['location'] = {
                    '$near': {
                        '$geometry': {
                            'type': 'Point',
                            'coordinates': [lon, lat],
                        },
                    }
                }
                if filters.get('min_distance') is not None:
                    mongo_filter['location']['$near']['$minDistance'] = (
                        float(filters['min_distance']))
                elif filters.get('max_distance') is not None:
                    mongo_filter['location']['$near']['$maxDistance'] = (
                        float(filters['max_distance']))
                else:
                    # Use a 5km radius by default
                    mongo_filter['location']['$near']['$maxDistance'] = 5000
            elif key in ['min_distance', 'max_distance']:
                if not filters.get('near'):
                    raise exception.Invalid(
                        "Distance parameters without reference point.")
            else:
                unrecognized_filters[key] = value

        if unrecognized_filters:
            raise exception.Invalid(
                "Unsupported filters: %s" % unrecognized_filters)

        stores = self._stores.find(mongo_filter, limit=1000)
        return list(stores)
