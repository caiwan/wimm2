import peewee
import components

class Category(components.BaseDocumentModel):
    title = peewee.TextField()
    comment = peewee.TextField(default = '')
    order = peewee.IntegerField(default=0)
    parent = peewee.ForeignKeyField('self', backref='children', null=True)
