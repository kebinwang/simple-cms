import datetime

from peewee import CharField, ForeignKeyField, DateTimeField
from flask_login import current_user

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    title = CharField(max_length=120)

    @classmethod
    def create_new(self, title):
        return Magazine.create(title=title)

    @classmethod
    def all(self):
        return Magazine.select()

    def update_posts(self, new_data):
        # remove old post
        query = MagazinePost.delete().where(MagazinePost.magazine == self.id)
        query.execute()
        # and new post
        for post_data in new_data:
            MagazinePost.create_new(
                user=current_user.id,
                magazine=self.id,
                title=post_data.get('title'),
                desc=post_data.get('desc'),
                url=post_data.get('url'),
                cover=post_data.get('cover'),
                category=post_data.get('category'),
                category_icon=post_data.get('category_icon'))


class MagazinePost(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine, related_name='posts')
    title = CharField(max_length=120)
    desc = CharField(max_length=400)
    url = CharField(max_length=200)
    cover = CharField(max_length=200)
    category = CharField(max_length=200)
    category_icon = CharField(max_length=200)

    @classmethod
    def create_new(self, user, magazine, title, desc, url,
                   cover, category, category_icon):
        return MagazinePost.create(
            user=user,
            magazine=magazine,
            title=title,
            desc=desc,
            url=url,
            cover=cover,
            category=category,
            category_icon=category_icon)
