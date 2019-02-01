# coding=utf-8
import io
from itertools import groupby
from csv import DictReader

from calendar import mdays
from datetime import datetime, timedelta
from playhouse.shortcuts import dict_to_model, model_to_dict

from app from app import components
from app.items.model import Item, TaggedItem
from app.categories.model import Category
from app.categories import categoryService
from app.tags import TagService


class ItemService(components.Service):
    _model_class = Item
    _name = "items"

    tagService = TagService()

    _DATE_FMT = "%Y-%m-%d"

    def _group_by_date(self, result):
        date_items = {}

        for date, items in groupby(result, lambda x: x["date"]):
            if date not in date_items:
                date_items[date] = []
            for item in items:
                date_items[date].append(item)

        # Because order can be suck sometimes
        date_item_list = []
        for date, items in date_items.items():
            date_item_list.append({"date": date, "items": items})
        return date_item_list

    def fetch_all_items(self, fetch_month=None, fetch_range=None):
        assert bool(fetch_month) != bool(fetch_range)

        def rq(fetch_from, fetch_to): return Item.select().where(
            Item.is_deleted == False,
            Item.date.between(fetch_from, fetch_to)
        ).order_by(Item.created.desc())

        if fetch_month:
            fetch_from = datetime(fetch_month[0], fetch_month[1], 1)
            fetch_to = fetch_from + timedelta(mdays[fetch_month[1]])
            return rq(fetch_from, fetch_to)

        elif fetch_range:
            fetch_range = [datetime.strptime(date, self._DATE_FMT) for date in fetch_range]
            return rq(*fetch_range)

        else:
            return Item.select().where(Item.is_deleted == False).order_by(Item.created.desc())

    def find_by_category(self, category_id):
        return Item.select().where(
            Item.category.id == category_id,
            Item.is_deleted == False
        ).order_by(Item.created.desc())

    def find_by_category_subtree(self, category_id):
        (_, category_subtree) = categoryService.fetch_subtree_ids(category_id)
        return Item.select().where(
            Item.category.id << [category.id for category in category_subtree],
            Item.is_deleted == False
        ).order_by(Item.created.desc())

    def read_item(self, item_id):
        item = Item.get(Item.id == item_id,
                        Item.is_deleted == False)
        if not item:
            raise Item.DoesNotExist()
        return item

    def create_item(self, item_json):
        tags = []
        if "tags" in item_json:
            tags = self.tagService.bulk_search_or_insert(item_json["tags"])
            del item_json["tags"]
        if "date" in item_json:
            item_json["date"] = datetime.strptime(item_json["date"], self._DATE_FMT)
        else:
            raise RuntimeError("Date is missing")
        category = None
        if "category" in item_json and item_json["category"]:
            category = Category.get(Category.id == int(item_json["category"]["id"]), Category.is_deleted == False)
        item = dict_to_model(Item, item_json)
        item.save()
        item.tags.add(tags)
        item.category = category
        return item

    def bulk_create_items(self, items_json):
        counter = 0
        items = []
        with components.DB.atomic():
            for item_json in items_json:
                item = self.create_item(item_json)
                items.append(item)
                counter += 1
        return (counter, items)

    def csv_import_items(self, text):
        counter = 0
        items = []
        with components.DB.atomic():
            reader = DictReader(io.StringIO(text), delimiter=",")
            for item_json in reader:
                item_json["tags"] = [tag.strip() for tag in item_json["tags"].split(",")]

                category_name = None
                if "category" in item_json:
                    category_name = item_json["category"]
                    del item_json["category"]

                item = self.create_item(item_json)

                if not category_name:
                    raise RuntimeError("No category was given item_count: {}".format(counter))
                item.category = categoryService.find_by_name(category_name)
                if not item.category:
                    raise RuntimeError("Invalid category {} was given at item_count: {}".format(category_name, counter))
                item.save()

                items.append(item)
                counter += 1
        return (counter, items)

    def update_item(self, item_id, item_json):
        my_item = Item.get(Item.id == item_id, Item.is_deleted == False)
        if not my_item:
            raise RuntimeError("Item with Id not found")

        tags = []
        if "tags" in item_json:
            tags = self.tagService.bulk_search_or_insert(item_json["tags"])
            del item_json["tags"]
        if "date" in item_json:
            item_json["date"] = datetime.strptime(item_json["date"], self._DATE_FMT)
        else:
            raise RuntimeError("Date is missing")

        if my_item:
            item = dict_to_model(Item, item_json)
            item.id = my_item.id
            item.changed()
            item.save()
            item.tags.clear()
            item.tags.add(tags)
            return item

    def delete_item(self, item_id):
        my_item = Item.get(Item.id == int(item_id))
        if my_item:
            my_item.is_deleted = True
            my_item.changed()
            my_item.save()
            return my_item
        return None

    def serialize_item(self, item):
        item_json = model_to_dict(item)
        item_json["date"] = item.date.strftime(self._DATE_FMT)
        item_json["tags"] = [str(tag.tag) for tag in item.tags]
        if item.category:
            item_json["category"] = {"id": item.category.id, "name": item.category.name}
        else:
            item_json["category"] = None
        return item_json


itemService = ItemService()


class ItemReportService(components.Service):
    # ...
    pass


def init(app, api, models):
    from app.items.controller import ItemListController, ItemController, ItemImportController
    components.register_controllers(api, [ItemListController, ItemController, ItemImportController])
    models.extend([Item, TaggedItem])
