import logging

from flask import jsonify
from flask import request

from mongo_webapp_sample.api.controllers import base as base_controller
from mongo_webapp_sample.api.schema import stores as store_schema
from mongo_webapp_sample import exception
from mongo_webapp_sample import utils

LOG = logging.getLogger('mongo_webapp_sample')


class StoresController(base_controller.BaseAPIController):
    def setup(self):
        self.setup_routes()

    def setup_routes(self):
        self._app.add_url_rule('/stores',
                               methods=['POST'],
                               view_func=self.add_store)
        self._app.add_url_rule('/stores',
                               methods=['GET'],
                               view_func=self.list_stores)
        self._app.add_url_rule('/stores/<store_id>',
                               methods=['DELETE'],
                               view_func=self.delete_store)
        self._app.add_url_rule('/stores/<store_id>',
                               methods=['PUT'],
                               view_func=self.update_store)
        self._app.add_url_rule('/stores/<store_id>',
                               methods=['GET'],
                               view_func=self.get_store)

    def add_store(self):
        LOG.info("Adding store: %s" % request.data)

        self.validate_request(store_schema.add_store)

        store = request.get_json()
        created_store = self._db.add_store(store)

        return jsonify(created_store)

    def update_store(self, store_id):
        LOG.info("Updating store: %s %s" % (store_id, request.data))

        self.validate_request(store_schema.update_store)

        store_updates = request.get_json()
        updated_store = self._db.update_store(store_id, store_updates)
        if not updated_store:
            raise exception.NotFound()

        return jsonify(updated_store)

    def list_stores(self):
        filters = utils.filter_keys(
            request.args.to_dict(),
            ['name', 'description', 'text',
             'near', 'min_distance', 'max_distance'])

        results = self._db.list_stores(filters)
        return jsonify(results)

    def get_store(self, store_id):
        result = self._db.get_store(store_id)
        if not result:
            raise exception.NotFound()
        return jsonify(result)

    def delete_store(self, store_id):
        self._db.delete_store(store_id)
        return jsonify(dict(mesage="Operation succeeded."))
