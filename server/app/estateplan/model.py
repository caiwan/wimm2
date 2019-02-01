import peewee

from app from app import components
from app.items.model import Item
from app.categories.model import Category


BUDGET_PERIOD_CHOICES = [
    (1, "day"),
    (2, "week"),
    (3, "month"),
    (4, "quarter"),
    (5, "year")
]


class LastAssetCalculationCache(components.BaseModel):
    # References the last point when the saving/estate sum calculations were made
    # in order to determine if update needed
    last_value = peewee.FloatField(null=False)
    last_item = peewee.ForeignKeyField(Item, null=False)
    pass


class Budget(components.BaseDocumentModel):
    title = peewee.TextField()
    period = peewee.IntegerField(default=0)
    amount = peewee.FloatField(null=False)
    target = peewee.ForeignKeyField(Category, null=True)
    cache = peewee.ForeignKeyField(LastAssetCalculationCache, null=True)


class Asset(components.BaseDocumentModel):
    # when positive estate value is given then it's interpreted as saving, and
    # when negative estate value is given then it's a debt record

    title = peewee.TextField()
    initial_amount = peewee.FloatField(null=True)
    goal = peewee.FloatField(null=True)
    end_date = peewee.DateTimeField(null=True)
    target = peewee.ForeignKeyField(Category, null=True)
    cache = peewee.ForeignKeyField(LastAssetCalculationCache, null=True)
