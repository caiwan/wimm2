from unittest import TestCase
import os, sys, io
from chrono import Timer
import json
import random


import logging
import peewee

import app
import components

from categories import categoryService
from categories import model as categoryModel


API_BASE = components.BASE_PATH
FILE_ROOT = os.path.dirname(__file__)


class CategoryImportExportTest(TestCase):

    post_args = {
        'content_type': 'application/json'
    }

    upload_args = {
        'content_type' : 'multipart/form-data'
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(':memory:')
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.app.test_client()

        self._import_categories()

    def tearDown(self):
        self._db.close()

    def test_flatten_categories(self):
        # given
        # - randomize all the data
        categories = categoryService.fetch_all_items()
        category_count = categoryService.fetch_all_items().count()
        random_category_order = {}
        with components.DB.atomic():
            for (category, random_order_id) in zip(categories, self._random_list(category_count)):
                category.flatten_order = random_order_id
                random_category_order[random_order_id] = category
                # logging.info('Reorder id={} flatten_order={}'.format(category.id, random_order_id))
                category.save()

        # - expect category order in random when select

        # when
        # - call flatten
        try:
            with Timer() as timed:
                categoryService._flatten_tree_order()
        except:
            logging.exception(sys.exc_info()[0])
            raise

        logging.info("Time spent: {} ms".format(timed.elapsed * 1000))

        # try:
            # for child in children:
                # logging.info('Order title={} id={} flatten_order={}'.format(child.title, child.id, child.flatten_order))

        # then
        # - expect categories be in order


    def _import_categories(self):
        source_filename = 'test_categories.json'
        with open(os.path.join(FILE_ROOT, 'assets', source_filename), encoding="utf-8") as f:
            text = f.read()
            json_file =  io.BytesIO(text.encode("utf-8"))
            json_data = json.loads(text)

            # when
            response = self.app.post(API_BASE+'/categories/upload/', data = {'file': (json_file, 'Untitled.json')}, **self.upload_args)
            self.assertEquals(200, response.status_code, msg = response.data)
            response_json = json.loads(response.data)

            self.assertEqual(len(response_json['items']), response_json['imported'])

            return response_json

    def _random_list(self, count):
        a = list(range(count))
        random.shuffle(a)
        return a

    def _validate_category(self, expected, actual):
        self.assertEqual(expected['title'], actual['title'])
        if expected['parent']:
            self.assertEqual(expected['parent']['id'], actual['parent']['id'])
        pass

