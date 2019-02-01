from unittest import TestCase
import ddt
import json
from datetime import datetime

import peewee

import app
from app from app import components

API_ROOT = components.BASE_PATH


@ddt.ddt
class AutocompleteTest(TestCase):
    args = {
        "content_type": "application/json"
    }

    DATE_FMT = "%Y-%m-%d"

    items = [
        {
            "date": datetime.now().strftime(DATE_FMT),
            "price": -999,
            "tags": ["these", "are", "the", "test", "tags", "we", "look", "for"]
        }, {
            "date": datetime.now().strftime(DATE_FMT),
            "price": -999,
            "tags": ["árvívz", "tűrő", "tükör", "fúró", "gép", "zsiráf", "oroszlán", "gepárd"]
        },
        {
            "date": datetime.now().strftime(DATE_FMT),
            "price": -999,
            "tags": ["This is something we don\"t expect to see, but", "we can have a tag like this", "and it still sohuld be valid", "as well"]
        }
    ]

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.APP.test_client()

        for item_data in self.items:
            response = self.app.post(API_ROOT + "/items/", data=json.dumps(item_data), **self.args)
            self.assertEquals(201, response.status_code)

        pass

    def tearDown(self):
        self._db.close()

    @ddt.unpack
    @ddt.data(
        ("the", ["these", "the"]),
        ("these", ["these"]),
        ("xoxoxo", []),
        ("árv", ["árvívz"]),
        ("This is something", ["This is something we don\"t expect to see, but"])
    )
    def test_autocomplete_query(self, query, expected_result):
        # given
        query_string = {"q": query}

        # when
        response = self.app.get(API_ROOT + "/autocomplete/", **self.args, query_string=query_string)
        self.assertEqual(200, response.status_code)

        # then
        response_json = json.loads(response.data)
        self.assertIsNotNone(response_json)

        # print ("oompa loompa " + response.data)

        for tag in expected_result:
            self.assertTrue(tag in response_json, tag)

        pass
