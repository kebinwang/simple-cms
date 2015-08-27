import datetime

from peewee import CharField, ForeignKeyField, DateTimeField, IntegerField
from flask_login import current_user

from .base import BaseModel
from .user import User


class Magazine(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    title = CharField(max_length=120)
    visits = IntegerField(default=0)

    class Meta:
        pass

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
                category_icon=post_data.get('categoryIcon'))

    def update_visits(self):
        self.visits += 1
        self.save()

    def dump(self):
        magazine_data = {}
        magazine_data['id'] = self.id
        magazine_data['title'] = self.title
        magazine_data['visits'] = self.visits
        magazine_data['posts'] = []
        magazine_data['create_time'] = self.create_time
        magazine_data['update_time'] = self.update_time

        magazine_posts = self.posts
        for magazine_post in magazine_posts:
            magazine_data['posts'].append(magazine_post.dump())
        return magazine_data


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

    class Meta:
        pass

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

    def dump(self):
        magazine_post_data = {}
        magazine_post_data['id'] = self.id
        magazine_post_data['title'] = self.title
        magazine_post_data['desc'] = self.desc
        magazine_post_data['url'] = self.url
        magazine_post_data['cover'] = self.cover
        magazine_post_data['category'] = self.category
        magazine_post_data['categoryIcon'] = self.category_icon
        magazine_post_data['create_time'] = self.create_time
        magazine_post_data['update_time'] = self.update_time

        return magazine_post_data
