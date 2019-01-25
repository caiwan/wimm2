from unittest import TestCase

import peewee

import app
from app import components

API_ROOT = components.BASE_PATH


class TagReportsTest(TestCase):
    args = {
        "content_type": "application/json"
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.APP.test_client()
        pass

    def tearDown(self):
        self._db.close()

    def test_tag_sum(self):
        self.fail("Not implemented")
        pass

    def test_tag_sum_over_time(self):
        self.fail("Not implemented")
        pass
