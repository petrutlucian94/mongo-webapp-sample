import logging

from flask import Flask
from flask import jsonify

from mongo_webapp_sample.api.controllers import stores
from mongo_webapp_sample import conf
from mongo_webapp_sample.db import api as db_api
from mongo_webapp_sample import exception


app = Flask(__name__)
LOG = logging.getLogger()


class MongoWebappSampleAPI:
    _api_controllers = [
        stores.StoresController,
    ]

    def setup(self):
        self._cfg = conf.get_cfg()

        self.setup_logging()
        self.setup_db()
        self.setup_controllers()

    def setup_logging(self):
        if self._cfg.debug:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        handler = logging.StreamHandler()
        handler.setLevel(log_level)

        log_fmt = '[%(asctime)s] %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_fmt)
        handler.setFormatter(formatter)

        LOG.addHandler(handler)
        LOG.setLevel(log_level)

    def setup_db(self):
        self._db = db_api.DatabaseAPI()
        # Ensure that the database is available.
        self._db.ping()
        self._db.initialize_indexes()

    def setup_controllers(self):
        for api_controller in self._api_controllers:
            api_controller(app, self._db).setup()

    @app.errorhandler(exception.WebappException)
    def generic_error_handler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        if conf.get_cfg().debug:
            LOG.exception(error)

        return response


def register_app():
    api = MongoWebappSampleAPI()
    api.setup()
    return app


def main():
    register_app()
    app.run()


if __name__ == '__main__':
    main()
