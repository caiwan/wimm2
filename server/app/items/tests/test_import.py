from datetime import datetime
import csv
import json
from unittest import TestCase
import os, io

import peewee

import app
import components

from items.model import Item

API_ROOT = components.BASE_PATH
FILE_ROOT = os.path.dirname(__file__)


def from_csv(filename):
    with open(os.path.join(FILE_ROOT, 'assets', filename), encoding="utf-8") as f:
        text = f.read()
        stream = io.BytesIO(text.encode("utf-8"))
        reader = csv.DictReader(io.StringIO(text), delimiter=',')
        items = [item for item in reader]
        return (stream, items)
    pass


class ImportItemTest(TestCase):
    args = {
        'content_type' : 'multipart/form-data'
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(':memory:')
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.app.test_client()
        pass

    def tearDown(self):
        self._db.close()

    def test_import_csv(self):
        # given
        (content, data) = from_csv("import_data.csv")

        # when
        response = self.app.post(API_ROOT + "/items/upload/", data = {
            'file': (content, 'Untitled.csv')
        }, **self.args)

        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)

        # then
        self.assertEqual(len(data), len(response_json['items']))

        pass
