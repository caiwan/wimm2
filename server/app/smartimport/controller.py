from flask import request
import components

from smartimport import smartImportService

class SmartImportUploadController(components.Controller):
    path = '/smartimport/upload/'
    _service = smartImportService

    def post(self):
        if 'file' not in request.files:
            return ({'error':'No uploaded file'}, 400)
        try: 
            uploaded_file = request.files['file']
            upload_type = str(request.form['type'])
            text = uploaded_file.read().decode(encoding='UTF-8',errors='strict')

            items = self._service.dispatch_import(upload_type, text)
            
            return ({
                'imported' : len(items), 
                'items' : [self._service.serialize_item(item) for item in items] 
                }, 200)

        except Exception as e :
            return ({'error':str(e)}, 400)


class SmartImportListController(components.Controller):
    path = '/smartimport/'
    _service = smartImportService

    def get(self):
        try :
            items = self._service.fetch_all_unfinished_items()

            return ({
                'imported' : len(items), 
                'items' : [self._service.serialize_item(item) for item in items] 
                }, 200)

        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)

        return self._service.get_unfinished_items()

    def post(self):
        try:
            items = self._service.bulk_store_items(request.json) 
            return ({
                'saved' : len(items), 
                'items' : [self._service.serialize_item(item) for item in items] 
                }, 200 )
        except RuntimeError as e:
            logging.exception("Bad request: " + str(e))
            return ({'error':str(e)}, 400)



class SmartImportController(components.Controller):
    path = '/smartimport/<int:item_id>/'
    _service = smartImportService

    def get(self, item_id):
        return self._read_item(item_id)
    
    def delete(self, item_id):
        return self._delete(item_id)

    def post(self, item_id):
        item = self._service.store_item(item_id, request.json)
        return self._service.serialize_item(item)

    def put(self, item_id):
        item = self._service.store_item(item_id, request.json)
        return self._service.serialize_item(item)

    def patch(self, item_id):
        item = self._service.store_item(item_id, request.json)
        return self._service.serialize_item(item)

    