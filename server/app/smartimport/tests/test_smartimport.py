# coding: utf-8

from datetime import datetime
import csv, json
import io, os
from unittest import TestCase

import ddt

import peewee

import app
import components

from categories import categoryService

API_ROOT = components.BASE_PATH
FILE_ROOT = os.path.dirname(__file__)
APP_ROOT = app.APP_ROOT

@ddt.ddt
class SmartImportTest(TestCase):
    args = {
        'content_type' : 'application/json'
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

        self._insert_categories("categories.json")

        pass

    def tearDown(self):
        self._db.close()

    @ddt.unpack
    @ddt.data(
        {'upload_type' : 1, 'source_filename' : 'otp.csv'}
    )
    def test_import_csv(self, upload_type, source_filename):
        # given
        with open(os.path.join(FILE_ROOT, 'assets', source_filename), encoding="utf-8") as f:
            text = f.read()
            csv_file = io.BytesIO(text.encode("utf-8"))
            csv_data = csv.DictReader(io.StringIO(text), delimiter=',')

            # when
            response = self.app.post(API_ROOT + '/smartimport/upload/',
                data = {'file': (csv_file, 'Untitled.csv'), 'type' : upload_type},
                **self.upload_args
            )
            self.assertEqual(200, response.status_code, msg=response.data)

            response_json = json.loads(response.data)

            # then
            self.assertTrue('imported' in response_json)
            self.assertTrue('items' in response_json)

            self.assertNotEqual(0, response_json['imported'])
            self.assertEqual(len(response_json['items']), response_json['imported'])

            self._validate_items(response_json['items'])

    @ddt.unpack
    @ddt.data(
        {'upload_type' : 1, 'source_filename' : 'otp.csv'}
    )
    def test_resume_editing(self, upload_type, source_filename):
        # given
        with open(os.path.join(FILE_ROOT, 'assets', source_filename), encoding="utf-8") as f:
            text = f.read()
            csv_file = io.BytesIO(text.encode("utf-8"))
            csv_data = csv.DictReader(io.StringIO(text), delimiter=',')

            response_json = self._upload_items(upload_type, csv_file)
            self._validate_items(response_json['items'])


        # when
        response = self.app.get(API_ROOT + '/smartimport/', **self.upload_args)

        # then
        self.assertEqual(200, response.status_code, msg=response.data)

        response_json = json.loads(response.data)

        self.assertTrue('imported' in response_json)
        self.assertTrue('items' in response_json)

        self._validate_items(response_json['items'])

    @ddt.unpack
    @ddt.data(
        {'upload_type' : 1, 'source_filename' : 'otp.csv', 'save_filename' : 'otp_save.csv'}
    )
    def test_save_item(self, upload_type, source_filename, save_filename):
        # given
        imported_item_ids = []
        with open(os.path.join(FILE_ROOT, 'assets', source_filename), encoding="utf-8") as f:
            text = f.read()
            csv_file = io.BytesIO(text.encode("utf-8"))
            csv_data = csv.DictReader(io.StringIO(text), delimiter=',')

            response_json = self._upload_items(upload_type, csv_file)
            imported_item_ids = [json['id'] for json in response_json['items']]
            self.assertEqual(len(imported_item_ids), response_json['imported'])

        # when
        with open(os.path.join(FILE_ROOT, 'assets', save_filename), encoding="utf-8") as f:
            text = f.read()
            csv_data = csv.DictReader(io.StringIO(text), delimiter=',')
            for item_pair in zip(imported_item_ids, csv_data):
                # print(item_pair)
                id = item_pair[0]
                item_json = item_pair[1]
                item_json['category'] = self._findCategory(item_json['category'])
                item_json['tags'] = item_json['tags'].split(',')
                response = self.app.post(API_ROOT + '/smartimport/'+str(id)+'/', data = json.dumps(item_json), **self.args)
                self.assertEqual(200, response.status_code, msg=response.data)

                response_json = json.loads(response.data)

                self.assertTrue('stored_item' in response_json)
                self.assertNotEqual(None, response_json['stored_item'])
                # TODO: check data

                pass

        # then

        pass


    def _validate_items(self, items):
        for item in items:
            self.assertTrue('id' in item)
            self.assertTrue('date' in item)
            self.assertTrue('price' in item)
            self.assertTrue('text' in item)
            self.assertTrue('suggested_tags' in item)
            self.assertTrue('suggested_category' in item)

    def _upload_items(self, upload_type, csv_file):
        response = self.app.post(API_ROOT + '/smartimport/upload/',
            data = {'file': (csv_file, 'Untitled.csv'), 'type' : upload_type},
            **self.upload_args
        )
        self.assertEqual(200, response.status_code, msg=response.data)

        response_json = json.loads(response.data)

        self.assertTrue('imported' in response_json)
        self.assertTrue('items' in response_json)

        self.assertNotEqual(0, response_json['imported'])
        self.assertEqual(len(response_json['items']), response_json['imported'])

        return response_json

    def _insert_categories(self,json_filename):
        with open(os.path.join(APP_ROOT, 'tests', 'assets', json_filename), encoding="utf-8") as f:
            json_data = json.loads(f.read())
            categoryService.bulk_create_items(json_data)

    def _findCategory(self, category_name):
        category = categoryService.find_by_title(category_name.lower())
        return {"id": category.id} if category else None
