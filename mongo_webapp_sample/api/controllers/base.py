import logging

from flask import request
import jsonschema

from mongo_webapp_sample import exception

LOG = logging.getLogger('mongo_webapp_sample')


class BaseAPIController(object):
    def __init__(self, flask_app, db):
        self._app = flask_app
        self._db = db

    def validate_schema(self, instance, schema):
        try:
            jsonschema.validate(instance=instance, schema=schema)
        except Exception as ex:
            raise exception.SchemaValidationError(reason=ex)

    def validate_request(self, schema):
        request_data = request.get_json()
        self.validate_schema(request_data, schema)

    def setup(self):
        pass
