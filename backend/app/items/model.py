import peewee

from app import components
from app.tags.model import Tag
from app.categories.model import Category


class Item(components.BaseDocumentModel):
    date = peewee.DateField(null=False)
    price = peewee.FloatField(null=False)
    tags = peewee.ManyToManyField(Tag)
    category = peewee.ForeignKeyField(Category, null=True)
    pass


TaggedItem = Item.tags.get_through_model()
