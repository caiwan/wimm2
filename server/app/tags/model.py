# coding=utf-8

import peewee

from app from app import components


class Tag(components.BaseModel):
    tag = peewee.TextField(null=False, unique=True)


class FuzzyTag(components.BaseModel):
    tag = peewee.ForeignKeyField(Tag)
    fuzzy = peewee.TextField(null=False)
    type = peewee.IntegerField(null=False)
