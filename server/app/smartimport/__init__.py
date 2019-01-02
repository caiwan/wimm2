# coding=utf-8
import io

from playhouse.shortcuts import *

import components

from smartimport.model import SmartImportedItem
from smartimport.parsers import dispatch as dispatch_import

from items import itemService


class SmartImportService(components.Service):
    _model_class = SmartImportedItem

    def fetch_all_unfinished_items(self):
        return SmartImportedItem.select().where(SmartImportedItem.is_deleted == False, SmartImportedItem.stored_item == None)

    def bulk_store_items(items_json):
        items = []
        with components.DB.atomic():
            for item_json in items_json:
                item = self.store_item(item_json['id'], item_json['item'])
                items.append(item)
        return items

    def store_item(self, item_id, item_json):
        item = self.read_item(item_id)

        item.stored_item = None
        if item.stored_item:
            item.stored_item = itemService.update_item(item.stored_item.id, item_json)
        else:
            item.stored_item = itemService.create_item(item_json)

        item.save()

        return item()

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
            item_json['stored_item'] = itemService.serialize_item(item.stored_item)

        if item.suggested_tags:
            item_json['suggested_tags'] = [str(tag.tag) for tag in item.tags]
        else:
            item_json['suggested_tags'] = []

        if item.suggested_category:
            item_json['suggested_cateogry'] = {'id' : item.category.id, 'title': item.category.title}
        else:
            item_json['suggested_category'] = None

        return item_json

    def _sanitize_item(self, item_json):
        suggested_tags = []
        if 'suggested_tags' in item_json:
            suggested_tags = item_json['suggested_tags']
            del item_json['suggested_tags']

        suggested_category = None
        if 'suggested_category' in item_json:
            suggested_category = item_json['suggested_category']
            del item_json['suggested_category']

        stored_item_json = None
        if 'stored_item' in item_json:
            stored_item_json = item_json['stored_item']
            del item_json['stored_item']

        return (item_json, suggested_tags, suggested_category, stored_item_json)

    pass


smartImportService = SmartImportService()


def init(app, api, models):
    from smartimport.model import TaggedSmartImportedItem
    from smartimport.controller import SmartImportUploadController
    from smartimport.controller import SmartImportListController, SmartImportController
    components.register_controllers(api, [SmartImportUploadController, SmartImportListController, SmartImportController])
    models.extend([SmartImportedItem, TaggedSmartImportedItem])
