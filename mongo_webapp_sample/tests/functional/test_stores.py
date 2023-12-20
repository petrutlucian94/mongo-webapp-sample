import json

from mongo_webapp_sample import exception
from mongo_webapp_sample.tests import fake_stores
from mongo_webapp_sample.tests.functional import test_base


class TestStores(test_base.BaseFunctionalTestCase):
    def _create_stores(self):
        self._created_stores = {}

        for store in fake_stores.stores_dict.values():
            result = self._client.post('/stores', json=store).text
            out_store = json.loads(result)
            self._created_stores[out_store['name']] = out_store

    def setUp(self):
        super().setUp()

        self._create_stores()

    def tearDown(self):
        self._db_api.delete_collection('stores')

        super().tearDown()

    def test_list_stores(self):
        reply = self._client.get('/stores').text
        out_stores = json.loads(reply)

        self.assertEqual(
            len(fake_stores.stores_dict),
            len(out_stores))

        for out_store in out_stores:
            store_name = out_store['name']
            exp_store = self._created_stores[store_name]
            self.assertDictEqual(exp_store, out_store)

    def test_text_search(self):
        reply = self._client.get('/stores?text=wand').text
        out_stores = json.loads(reply)

        exp_stores = [
            self._created_stores[fake_stores.olivanders_store['name']]]
        self.assertCountEqual(out_stores, exp_stores)

        reply = self._client.get('/stores?text=restaurant').text
        out_stores = json.loads(reply)

        exp_stores = [
            self._created_stores[fake_stores.los_pollos_store['name']],
            self._created_stores[fake_stores.mos_eisley_store['name']]
        ]
        self.assertCountEqual(out_stores, exp_stores)

    def test_geospatial_search(self):
        reply = self._client.get(
            '/stores?near=21.2283754,45.74102&max_distance=5000').text
        out_stores = json.loads(reply)

        exp_stores = [
            self._created_stores[fake_stores.wonkas_store['name']],
            self._created_stores[fake_stores.olivanders_store['name']],
            self._created_stores[fake_stores.mos_eisley_store['name']]
        ]
        self.assertCountEqual(out_stores, exp_stores)

    def test_delete(self):
        deleted_store = self._created_stores[
            fake_stores.wonkas_store['name']]
        self._client.delete('/stores/%s' % deleted_store['_id'])

        self.assertRaises(exception.RequestFailed,
                          self._client.get,
                          '/stores/%s' % deleted_store['_id'])

    def test_update(self):
        store = self._created_stores[fake_stores.los_pollos_store['name']]
        updates = dict(Name="Gustavo's BBQ")
        exp_store = dict(store, **updates)

        reply = self._client.put(
            '/stores/%s' % store['_id'], json=updates).text
        # check PUT reply
        out_store = json.loads(reply)

        reply = self._client.get('/stores/%s' % store['_id']).text
        out_store = json.loads(reply)
        # check GET reply
        self.assertEqual(exp_store, out_store)
