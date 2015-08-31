import datetime

from peewee import CharField, ForeignKeyField, DateTimeField

from .base import BaseModel
from .user import User
from .post import Post


class Magazine(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    title = CharField(max_length=120)

    @classmethod
    def create_magazine(self, title):
        return Magazine.create(title=title)

    @classmethod
    def all(self):
        return Magazine.select()

    def update_magazine(self, title):
        self.title = title
        self.save()


class MagazinePost(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine, related_name='posts')
    post = ForeignKeyField(Post, related_name='magazine_posts')
    title = CharField(max_length=120)
    desc = CharField(max_length=400)
    cover = CharField(max_length=200)
    category = CharField(max_length=200)
    category_icon = CharField(max_length=200)

    class Meta:
        order_by = ('-create_time',)

    @classmethod
    def create_magazine_post(self, user_id, magazine_id, post_id, title, desc,
                             cover, category, category_icon):
        return MagazinePost.create(
            user=user_id,
            magazine=magazine_id,
            post=post_id,
            title=title,
            desc=desc,
            cover=cover,
            category=category,
            category_icon=category_icon)

    def update_magazine_post(self, user_id, magazine_id, post_id, title, desc,
                             cover, category, category_icon):
        self.user = user_id
        self.magazine = magazine_id
        self.post = post_id
        self.title = title
        self.desc = desc
        self.cover = cover
        self.category = category
        self.category_icon = category_icon
        self.save()
