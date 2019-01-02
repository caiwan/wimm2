import peewee
import components

from categories.model import Category


BUDGET_PERIOD_CHOICES = [
    (1, 'day'),
    (2, 'week'),
    (2, 'month'),
    (2, 'quarter')
]


class Budget(components.BaseDocumentModel):
    title = peewee.TextField()
    period = peewee.IntegerField(default=0)
    amount = peewee.FloatField(null=False)
    target = peewee.ForeignKeyField(Category, null=True)


class Saving(components.BaseDocumentModel):
    # when negative goal is given then it turns into a debt record 
    title = peewee.TextField()
    initial_amount = peewee.FloatField(null=True)
    goal = peewee.FloatField(null=True)
    end_date = peewee.DateTimeField(null=True)
    target = peewee.ForeignKeyField(Category, null=True)

