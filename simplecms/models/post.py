import datetime

from peewee import CharField, TextField, ForeignKeyField, DateTimeField

from .base import BaseModel
from .user import User


class Post(BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    user = ForeignKeyField(User)
    author_name = CharField(max_length=60)
    category = CharField(max_length=60)
    title = CharField(max_length=120)
    content = TextField()

    @classmethod
    def create_new(self, user, author_name, category, title, content):
        return Post.create(
            user=user,
            author_name=author_name,
            category=category,
            title=title,
            content=content)

    @classmethod
    def all(self):
        return Post.select()

    def update_post(self, new_data):
        self.author_name = new_data.get('author')
        self.category = new_data.get('category')
        self.title = new_data.get('title')
        self.content = new_data.get('content')
        self.save()
