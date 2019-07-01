# coding=utf-8
import logging
import io

from playhouse.shortcuts import dict_to_model, model_to_dict

from app import components

from app.smartimport.model import SmartImportedItem
from app.smartimport.parsers import dispatch as dispatch_import
from app.items import itemService


class SmartImportService(components.Service):
    _model_class = SmartImportedItem

    _DATE_FMT = "%Y-%m-%d"

    def fetch_all_unfinished_items(self):
        return SmartImportedItem.select().where(SmartImportedItem.is_deleted == False, SmartImportedItem.stored_item == None)

    def bulk_store_items(self, items_json):
        items = []
        with components.DB.atomic():
            for item_json in items_json:
                item = self.store_item(item_json["id"], item_json["item"])
                items.append(item)
        return items

    def store_item(self, item_id, item_json):
        item = self.read_item(item_id)

        if item and item.stored_item:
            logging.info("Update stored item id={} stored_id={}".format(item_id, item.stored_item.id))
            item.stored_item = itemService.update_item(item.stored_item.id, item_json)
        else:
            logging.info("Create stored item id={}".format(item_id))
            item.stored_item = itemService.create_item(item_json)

        item.save()

        return item

    def create_item(self, item_json):
        (item_json, suggested_tags, suggested_category, stored_item_json) = self._sanitize_item(item_json)

        item = dict_to_model(SmartImportedItem, item_json)

        # TODO: Take care of the rest, eg: tags, category
        item.save()

        return item

    def dispatch_import(self, importer_type, text):
        importer = dispatch_import(importer_type)
        if not importer:
            raise RuntimeError("Invlaid parser or not found")

        imported_items = importer.preprocess(io.StringIO(text))
        items = []
        with components.DB.atomic():
            for imported_item in imported_items:
                item = self.create_item(imported_item)
                importer.make_suggestion(item)
                item.save()
                items.append(item)

        return items

    def serialize_item(self, item):
        item_json = model_to_dict(item)

        if item.stored_item:
            item_json["stored_item"] = itemService.serialize_item(item.stored_item)

        if item.suggested_tags:
            item_json["suggested_tags"] = [str(tag.tag) for tag in item.tags]
        else:
            item_json["suggested_tags"] = []

        if item.suggested_category:
            item_json["suggested_category"] = {"id": item.category.id, "title": item.category.title}
        else:
            item_json["suggested_category"] = None

        item_json["date"] = item.date.strftime(self._DATE_FMT)

        return item_json

    def _sanitize_item(self, item_json):
        suggested_tags = []
        if "suggested_tags" in item_json:
            suggested_tags = item_json["suggested_tags"]
            del item_json["suggested_tags"]

        suggested_category = None
        if "suggested_category" in item_json:
            suggested_category = item_json["suggested_category"]
            del item_json["suggested_category"]

        stored_item_json = None
        if "stored_item" in item_json:
            stored_item_json = item_json["stored_item"]
            del item_json["stored_item"]

        return (item_json, suggested_tags, suggested_category, stored_item_json)

    pass


smartImportService = SmartImportService()


class Module (components.Module):
    from app.smartimport.model import TaggedSmartImportedItem
    from app.smartimport.controller import SmartImportUploadController
    from app.smartimport.controller import SmartImportListController, SmartImportController
    name = "smartimport"
    services = [smartImportService]
    models = [TaggedSmartImportedItem]
    controllers = [SmartImportUploadController, SmartImportListController, SmartImportController]


module = Module()
