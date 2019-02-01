import json
import os
import io
from datetime import datetime
from unittest import TestCase

import peewee

import app
from app from app import components

from app.categories import categoryService

from app.tests.utils import from_csv

API_ROOT = components.BASE_PATH
FILE_ROOT = os.path.dirname(__file__)
APP_ROOT = app.APP_ROOT


class ImportItemTest(TestCase):
    args = {
        "content_type": "multipart/form-data"
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.APP.test_client()

        self._insert_categories("categories.json")

    def tearDown(self):
        self._db.close()

    def test_import_csv(self):
        # given
        (content, data) = from_csv(FILE_ROOT, "assets", "import_data.csv")

        # when
        response = self.app.post(API_ROOT + "/items/upload/", data={
            "file": (content, "Untitled.csv")
        }, **self.args)

        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)

        # then
        self.assertEqual(len(data), len(response_json["items"]))

    def _insert_categories(self, json_filename):
        with open(os.path.join(APP_ROOT, "tests", "assets", json_filename), encoding="utf-8") as f:
            json_data = json.loads(f.read())
            categoryService.bulk_create_items(json_data)
