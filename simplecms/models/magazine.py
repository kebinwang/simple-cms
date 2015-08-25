from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    title = CharField()

    class Meta:
        order_by = ('-id',)

    @classmethod
    def get_all_magazines(self):
        return list(Magazine.select())


class MagazinePost(BaseModel):
    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine)
    title = CharField()
    desc = CharField()
    url = CharField()
    cover = CharField()
    category = CharField()
    categoryIcon = CharField()

    class Meta:
        order_by = ('-id',)

    #TODO: 能不能用 peewee 自带的方法简便的完成？比如像访问对象的内容一样通过 Magazine 直接访问 Magazine 的 POST
    @classmethod
    def get_post_with_magazine_id(self, id):
        return list(MagazinePost.select().where(MagazinePost.magazine == id))
