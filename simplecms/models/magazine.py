from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    title = TextField()

    class Meta:
        order_by = ('-id',)


class MagazinePost(BaseModel):
    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine)
    title = TextField()
    desc = TextField()
    url = CharField()
    cover = CharField()
    category = CharField()
    categoryIcon = CharField()

    class Meta:
        order_by = ('-id',)
