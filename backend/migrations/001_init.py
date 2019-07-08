"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

from datetime import datetime
from uuid import uuid4
import peewee
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = peewee.SQL


def migrate(migrator, database, fake=False, **kwargs):
    class BaseModel(peewee.Model):
        pass

    @migrator.create_model
    class Role(BaseModel):
        name = peewee.TextField(null=False, unique=True)
        pass

    @migrator.create_model
    class User(BaseModel):
        class Meta:
            table_name = "users"

        name = peewee.TextField(null=False, index=True, unique=True)
        password = peewee.TextField(null=False)

        display_name = peewee.TextField(null=True)
        created = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
        edited = peewee.DateTimeField(null=False, default=datetime.now, index=True, formats=["%s"])

        user_ref_id = peewee.UUIDField(null=False, unique=True, index=True, default=uuid4)
        is_deleted = peewee.BooleanField(null=False, default=False)
        is_active = peewee.BooleanField(null=False, default=False)

        permissions = peewee.ManyToManyField(Role, backref="users")

    migrator.create_model(User.permissions.through_model)

    @migrator.create_model
    class Token(BaseModel):
        user = peewee.ForeignKeyField(User)
        issued_at = peewee.DateTimeField(null=False, default=datetime.now)
        expiration = peewee.DateTimeField(null=False)
        jwt = peewee.TextField(null=False)

    class BaseDocumentModel(BaseModel):
        created = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
        edited = peewee.DateTimeField(null=False, default=datetime.now, index=True, formats=["%s"])
        is_deleted = peewee.BooleanField(null=False, default=False)
        owner = peewee.ForeignKeyField(User, null=True)

    # Category
    @migrator.create_model
    class Category(BaseDocumentModel):
        name = peewee.TextField()
        comment = peewee.TextField(default="")
        is_archived = peewee.BooleanField(default=False)
        is_protected = peewee.BooleanField(default=False)
        order = peewee.IntegerField(default=0)
        path = peewee.TextField()
        parent = peewee.ForeignKeyField("self", backref="children", null=True)

    # Tags
    @migrator.create_model
    class Tag(BaseModel):
        tag = peewee.TextField(null=False)
        owner = peewee.ForeignKeyField(User)

    @migrator.create_model
    class FuzzyTag(BaseModel):
        tag = peewee.ForeignKeyField(Tag)
        fuzzy = peewee.TextField(null=False)

    # Items
    @migrator.create_model
    class Item(BaseDocumentModel):
        date = peewee.DateField(null=False)
        price = peewee.FloatField(null=False)
        tags = peewee.ManyToManyField(Tag)
        category = peewee.ForeignKeyField(Category, null=True)

    migrator.create_model(Item.tags.get_through_model())

    @migrator.create_model
    class SmartImportedItem(BaseDocumentModel):
        text = peewee.TextField()
        type = peewee.IntegerField(null=False, default=0)
        date = peewee.DateField(null=False, default=datetime.now)
        price = peewee.FloatField(null=False)
        suggested_tags = peewee.ManyToManyField(Tag)
        suggested_category = peewee.ForeignKeyField(Category, null=True)
        stored_item = peewee.ForeignKeyField(Item, null=True, default=None)

    migrator.create_model(SmartImportedItem.suggested_tags.get_through_model())


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
