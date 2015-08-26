from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    title = CharField(max_length=120)

    class Meta:
        order_by = ('-id',)

    @classmethod
    def create_new(self, title):
        return Magazine.create(title=title)

    @classmethod
    def all(self):
        return Magazine.select()

    @classmethod
    def dump_all(self):
        magazines = Magazine.all()
        magazines_data = []
        for magazine in magazines:
            magazines_data.append(magazine.dump())
        return magazines_data

    def dump(self):
        magazine_data = {}
        magazine_data['id'] = self.id
        magazine_data['title'] = self.title
        magazine_data['posts'] = []

        magazine_posts = self.posts
        for magazine_post in magazine_posts:
            magazine_data['posts'].append(magazine_post.dump())
        return magazine_data


class MagazinePost(BaseModel):
    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine, related_name='posts')
    title = CharField(max_length=120)
    desc = CharField(max_length=400)
    url = CharField(max_length=200)
    cover = CharField(max_length=200)
    category = CharField(max_length=200)
    category_icon = CharField(max_length=200)

    class Meta:
        order_by = ('-id',)

    @classmethod
    def create_new(self, user, magazine, title, desc, url, cover, category, category_icon):
        return MagazinePost.create(
            user=user,
            magazine=magazine,
            title=title,
            desc=desc,
            url=url,
            cover=cover,
            category=category,
            category_icon=category_icon)

    def dump(self):
        magazine_post_data = {}
        magazine_post_data['id'] = self.id
        magazine_post_data['title'] = self.title
        magazine_post_data['desc'] = self.desc
        magazine_post_data['url'] = self.url
        magazine_post_data['cover'] = self.cover
        magazine_post_data['category'] = self.category
        magazine_post_data['categoryIcon'] = self.category_icon
        return magazine_post_data
