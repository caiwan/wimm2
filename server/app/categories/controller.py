import logging 

from flask import request
import components

import json

from categories import categoryService


class CategoryListController(components.Controller):
    path = "/categories/"
    _service = categoryService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class CategoryController(components.Controller):
    path = "/categories/<int:category_id>/"
    _service = categoryService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)

class CategoryImportExportController(components.Controller):
    path = "/categories/import-export/"
    _service = categoryService

    def post(self):
        if 'file' not in request.files:
            return ({'error':'No uploaded file'}, 400)
        try: 
            uploaded_file = request.files['file']
            text = uploaded_file.read().decode(encoding='UTF-8',errors='strict')
            data_json = json.loads(text)

            items = self._service.bulk_create_items(data_json)
          
            return ({
                'imported': len(items), 
                'items': [self._service.serialize_item(item) for item in items]
            }, 200)
            
        except Exception as e :
            logging.exception(str(e))
            return ({'error':str(e)}, 400)
        pass

