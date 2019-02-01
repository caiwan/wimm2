from datetime import datetime

import peewee

from app from app import components
from app.items.model import Item
from app.categories.model import Category
from app.tags.model import Tag


class SmartImportedItem(components.BaseDocumentModel):
    text = peewee.TextField()
    type = peewee.IntegerField(null=False, default=0)
    date = peewee.DateField(null=False, default=datetime.now)
    price = peewee.FloatField(null=False)
    suggested_tags = peewee.ManyToManyField(Tag)
    suggested_category = peewee.ForeignKeyField(Category, null=True)
    stored_item = peewee.ForeignKeyField(Item, null=True, default=None)


TaggedSmartImportedItem = SmartImportedItem.suggested_tags.get_through_model()
