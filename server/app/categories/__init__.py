# coding=utf-8

import components
from categories.model import Category

class CategoryService(components.Service):
    _model_class = Category

    def fetch_all_items(self):
        return Category.select().where(Category.is_deleted == False).order_by(Category.order)

    def create_item(self, item_json):
        parent = None
        if 'parent' in item_json and 'id' in item_json['parent'] and item_json['parent']['id']:
            parent = self.read_item(int(item_json['parent']['id']))
            
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

categoryService = CategoryService()

def init(app, api, models):
    from categories.controller import CategoryController, CategoryListController
    components.register_controllers(api, [CategoryController, CategoryListController])
    models.extend([Category])
    pass
