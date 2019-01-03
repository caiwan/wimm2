# coding=utf-8

from playhouse.shortcuts import *

import components
from categories.model import Category

import logging

class CategoryService(components.Service):
    _model_class = Category

    def fetch_all_items(self):
        return Category.select().where(Category.is_deleted == False).order_by(Category.order)

    def create_item(self, item_json):
        parent = None
        if 'parent' in item_json:
            if item_json['parent'] and 'id' in item_json['parent']:
                id = int(item_json['parent']['id'])
                parent = self.read_item(id).get()
            del item_json['parent']
            
        item = dict_to_model(Category, item_json)
        item.parent = parent
        item.save()
        return item

    def edit_item(self, item_json):
        parent = None
        if 'parent' in item_json and 'id' in item_json['parent'] and item_json['parent']['id']:
            parent = self.read_item(item_json['parent'])
            
        item = dict_to_model(Category, item_json)
        item.parent = parent
        item.save()
        pass

    def merge_category(self, src_id, dst_id):
        pass

    def find_by_title(self, title):
        return Category.select().where(
            Category.title.contains(title),
            Category.is_deleted == False,
        ).objects()

    def fetch_all_children(self, item_id):
        result = []
        children_queue = Category.select().where(
            Category.parent.id == int(item_id),
            Category.is_deleted == False
        ).objects()

        # + recurse fetch all the children
        while children_queue:
            child = children_queue[:-1]
            children_queue = children_queue[0:-1]

            result.append(child)

            children = Category.select().where(
                Category.parent == child,
                Category.is_deleted == False
            ).objects()

            children_queue.extend(children)

        return result
        

    def bulk_create_items(self, items_json):
        parent_map = dict()
        item_map = dict()
        items = []
        with components.DB.atomic():
            for item_json in items_json:

                if 'id' not in item_json:
                    raise RuntimeError('ID is missing from one item')

                id = int(item_json['id'])

                parent_id = None 
                
                if 'parent' in item_json and item_json['parent']:
                    parent_id = int(item_json['parent']['id']) if 'id' in item_json['parent'] else None
                
                del item_json['id']
                del item_json['parent']

                parent_map[id] = parent_id

                item = self.create_item(item_json)
                item_map[id] = item
                items.append(item)
                
                logging.info("Insert item ID: {} item ID {}".format(id, item.id))

            for (item_id, parent_id) in parent_map.items():
                if parent_id:
                    item = item_map[item_id]
                    item.parent = item_map[parent_id]
                    logging.info("Attach parent {} <- {}".format(item_id, parent_id))
                    item.save()

            return items

        pass

categoryService = CategoryService()

def init(app, api, models):
    from categories.controller import CategoryController, CategoryListController 
    from categories.controller import CategoryImportExportController
    components.register_controllers(api, [CategoryController, CategoryListController, CategoryImportExportController])
    models.extend([Category])
    pass
