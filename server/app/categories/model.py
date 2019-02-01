import peewee

from app from app import components


class Category(components.BaseDocumentModel):
    name = peewee.TextField()
    comment = peewee.TextField(default="")
    order = peewee.IntegerField(default=0)
    flatten_order = peewee.IntegerField(default=0)
    parent = peewee.ForeignKeyField("self", backref="children", null=True)
