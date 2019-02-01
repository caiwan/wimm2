from unittest import TestCase
import os, io
import json

import peewee

import app
from app from app import components


API_BASE = components.BASE_PATH
FILE_ROOT = os.path.dirname(__file__)


class CategoryImportExportTest(TestCase):

    post_args = {
        "content_type": "application/json"
    }

    upload_args = {
        "content_type": "multipart/form-data"
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.APP.test_client()

    def tearDown(self):
        self._db.close()

    def test_import_categories(self):
        # given
        source_filename = "test_categories.json"
        with open(os.path.join(FILE_ROOT, "assets", source_filename), encoding="utf-8") as f:
            text = f.read()
            json_file = io.BytesIO(text.encode("utf-8"))
            # json_data = json.loads(text)

            # when
            response = self.app.post(API_BASE + "/categories/upload/", data={"file": (json_file, "Untitled.json")}, **self.upload_args)
            self.assertEquals(200, response.status_code, msg=response.data)
            response_json = json.loads(response.data)

            self.assertEqual(len(response_json["items"]), response_json["imported"])
            # imported_json = response_json

            # TODO: Validate data

            # TBD

            # response = self.app.get(API_BASE+"/categories/", **self.post_args)
            # self.assertEquals(200, response.status_code, msg = response.data)

            # then
            # for item in response_json["items"]:
            #   pass

            # self._validate_category(category, category_json)

    def _validate_category(self, expected, actual):
        self.assertEqual(expected["title"], actual["title"])
        if expected["parent"]:
            self.assertEqual(expected["parent"]["id"], actual["parent"]["id"])
        pass
