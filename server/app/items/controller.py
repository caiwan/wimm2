import logging

from flask_restful import request

from app from app import components
from app.items import itemService, ItemReportService


class ItemListController(components.Controller):
    path = "/items/"
    _service = itemService

    def get(self):
        query_year = request.args.get("year")
        query_month = request.args.get("month")

        query_from = request.args.get("from")
        query_to = request.args.get("to")

        result = []
        status = 503
        if query_year and query_month:
            (result, status) = self._fetch_all(fetch_month=(int(query_year), int(query_month)))
        elif query_from and query_to:
            (result, status) = self._fetch_all(fetch_range=(query_from, query_to))
        else:
            (result, status) = self._fetch_all()

        if status == 200:
            return (self._service._group_by_date(result), 200)

        return (result, status)

    def post(self):
        (result, status) = self._create(request.json)
        # if status == 201:
        #   return (self._service._group_by_date([result]), 201)
        return (result, status)

    def delete(self):
        for id in request.json["items"]:
            self._delete(int(id))
        return ("", 200)


class ItemController(components.Controller):
    path = "/items/<item_id>/"
    _service = itemService

    def get(self, item_id):
        (result, status) = self._read(item_id)
        return (result, status)

    def put(self, item_id):
        (result, status) = self._update(item_id, request.json)
        return (result, status)

    def patch(self, item_id):
        (result, status) = self._update(item_id, request.json)
        return (result, status)

    def delete(self, item_id):
        return self._delete(item_id)


class ItemImportController(components.Controller):
    path = "/items/upload/"
    _service = itemService

    def post(self):
        if "file" not in request.files:
            return ({"error": "No uploaded file"}, 400)
        try:
            uploaded_file = request.files["file"]
            text = uploaded_file.read().decode(encoding="UTF-8", errors="strict")
            (imported, items) = self._service.csv_import_items(text)
            items = [self._service.serialize_item(item) for item in items]
            return ({"imported": imported, "items": items}, 200)
        except Exception as e:
            logging.exception(e)
            return ({"error": str(e)}, 400)


class TagSumController(components.Controller):
    path = "/tag_sum/"
    _service = ItemReportService()

    def get(self):
        pass


class TagSumOverTimeController(components.Controller):
    path = "/tag_sum_over_time/"
    _service = ItemReportService()

    def get(self):
        pass
