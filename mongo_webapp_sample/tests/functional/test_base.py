import testtools
import threading
import uuid

from werkzeug import serving

from mongo_webapp_sample.cmd import api
from mongo_webapp_sample import conf
from mongo_webapp_sample.db import api as db_api
from mongo_webapp_sample.tests import http_client

TEST_SERVER_HOST = "127.0.0.1"
TEST_SERVER_PORT = 5001
HTTP_TIMEOUT = 5


class TestServer:
    def __init__(self, app, host, port):
        self.server = serving.make_server(
            host=host, port=port, app=app)

    def start(self):
        self.worker = threading.Thread(target=self.server.serve_forever)
        self.worker.start()

    def shutdown(self):
        self.server.shutdown()


class BaseFunctionalTestCase(testtools.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        addr = f"http://{TEST_SERVER_HOST}:{TEST_SERVER_PORT}"
        cls._client = http_client.HttpClient(
            addr, timeout=HTTP_TIMEOUT)

        # use a temporary mongo db
        test_db_name = 'test_%s' % uuid.uuid4().fields[0]
        conf.get_cfg().mongo_db_name = test_db_name

        cls._db_api = db_api.DatabaseAPI()

        # Spin up a temporary web server that will be used by the functional
        # tests. Make sure to pass a mongo uri through env variables.
        app = api.register_app()
        cls.server = TestServer(app, TEST_SERVER_HOST, TEST_SERVER_PORT)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls._db_api.delete_database()
