from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    title = CharField()

    class Meta:
        order_by = ('-id',)

    @classmethod
    def create_new(self, title):
        return Magazine.create(title=title)

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

    @classmethod
    def create_new(self, user, magazine, title, desc, url, cover, category, categoryIcon):
        return MagazinePost.create(
            user=user,
            magazine=magazine,
            title=title,
            desc=desc,
            url=url,
            cover=cover,
            category=category,
            categoryIcon=categoryIcon)

    #TODO: 能不能用 peewee 自带的方法简便的完成？比如像访问对象的内容一样通过 Magazine 直接访问 Magazine 的 POST
    @classmethod
    def get_post_with_magazine_id(self, id):
        return list(MagazinePost.select().where(MagazinePost.magazine == id))
