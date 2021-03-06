import datetime

from peewee import CharField, TextField, ForeignKeyField, DateTimeField,\
    IntegerField

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
    visits = IntegerField(default=0)

    class Meta:
        order_by = ('-create_time',)

    @classmethod
    def create_post(self, user_id, author_name, category, title, content):
        return Post.create(
            user=user_id,
            author_name=author_name,
            category=category,
            title=title,
            content=content)

    @classmethod
    def all(self):
        return Post.select()

    def update_visits(self):
        q = Post.update(visits=Post.visits + 1).where(Post.id == self.id)
        q.execute()

    def update_post(self, author_name, category, title, content):
        self.author_name = author_name
        self.category = category
        self.title = title
        self.content = content
        self.save()
