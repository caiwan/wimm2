from unittest import TestCase
import json

import peewee

import app
from app import components

from app.tests import BaseTest


API_ROOT = components.BASE_PATH


class ItemCRUDTest(BaseTest, TestCase):
    args = {
        "content_type": "application/json"
    }

    def __init__(self, methodName):
        BaseTest.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()
        pass

    def tearDown(self):
        self._db.close()

    def test_insert(self):
        # given
        item_data = {"date": "2018-11-14", "price": -999, "tags": ["tag1", "tag2"]}

        # when
        item_json = self._insert_item(item_data)

        # then
        self.assertIsNotNone(item_json)
        # .. okay for now
        pass

    def test_date_fetch(self):
        # given
        items_data = [
            {"date": "2018-11-15", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-11-16", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-10-09", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-09-09", "price": -999, "tags": ["tag1", "tag2"]},
        ]
        items_json = [self._insert_item(item_data) for item_data in items_data]
        # TODO: Validate Data

        # when
        response = self.app.get("{}/items/?year={}&month={}".format(API_ROOT, 2018, 11))
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        self.assertIsNotNone(response_json)

        # then
        self.assertEqual(2, len(response_json))
        self.assertEqual(1, len(response_json[0]["items"]))
        self.assertEqual(1, len(response_json[1]["items"]))

        pass

    def test_range_fetch(self):
        # given
        items_data = [
            {"date": "2018-11-15", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-11-16", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-10-09", "price": -999, "tags": ["tag1", "tag2"]},
            {"date": "2018-09-09", "price": -999, "tags": ["tag1", "tag2"]},
        ]
        items_json = [self._insert_item(item_data) for item_data in items_data]

        # TODO: Validate data`

        # when
        response = self.app.get("{}/items/?from={}&to={}".format(API_ROOT, "2018-10-01", "2018-11-30"))
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)
        self.assertIsNotNone(response_json)

        # then
        self.assertEqual(3, len(response_json))
        # self.assertEqual(1, len(response_json[0]["items"]))
        # self.assertEqual(1, len(response_json[1]["items"]))

        pass

    def test_update(self):
        # given
        item_data = {"date": "2018-11-14", "price": -999, "tags": ["tag1", "tag2"]}
        item_json = self._insert_item(item_data)
        item_id = item_json["id"]

        # when
        modified_item_data = {"date": "2018-01-01", "price": -9001, "tags": ["anothertag1", "anothertag2"]}

        response = self.app.patch(API_ROOT + "/items/" + str(item_id) + "/", data=json.dumps(modified_item_data), **self.args)
        self.assertEquals(200, response.status_code)
        # response_json = json.loads(response.data)

        # TODO: Validate data

        # then
        item_json = self._get_item(item_id)
        self.assertIsNotNone(item_json)
        # .. okay for now

        pass

    def test_delete(self):
        # given
        item_data = {"date": "2018-11-14", "price": -999, "tags": ["tag1", "tag2"]}
        item_json = self._insert_item(item_data)
        item_id = item_json["id"]

        # when
        response = self.app.delete(API_ROOT + "/items/" + str(item_id) + "/")
        self.assertEquals(200, response.status_code)

        # then
        response = self.app.get(API_ROOT + "/items/" + str(item_id) + "/", data=json.dumps(item_data), **self.args)
        self.assertEquals(404, response.status_code)

        pass

    def _get_item(self, item_id):
        response = self.app.get(API_ROOT + "/items/" + str(item_id) + "/", **self.args)
        self.assertEquals(200, response.status_code)
        response_json = json.loads(response.data)
        return response_json

    def _insert_item(self, item_data):
        response = self.app.post(API_ROOT + "/items/", data=json.dumps(item_data), **self.args)
        self.assertEquals(201, response.status_code)
        response_json = json.loads(response.data)
        return response_json
