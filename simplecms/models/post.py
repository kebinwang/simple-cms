import datetime

from peewee import CharField, TextField, ForeignKeyField, DateTimeField, IntegerField

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
        pass

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

    @classmethod
    def dump_list(self):
        posts = Post.all()
        posts_data = []
        for post in posts:
            posts_data.append(post.dump_desc())
        return posts_data

    def update_post(self, new_data):
        self.author_name = new_data.get('author')
        self.category = new_data.get('category')
        self.title = new_data.get('title')
        self.content = new_data.get('content')
        self.save()

    def update_visits(self):
        self.visits += 1
        self.save()

    def dump(self):
        post_data = {}
        post_data['id'] = self.id
        post_data['author'] = self.author_name
        post_data['category'] = self.category
        post_data['title'] = self.title
        post_data['content'] = self.content
        post_data['create_time'] = self.create_time
        post_data['update_time'] = self.update_time
        post_data['visits'] = self.visits
        return post_data

    def dump_desc(self):
        post_data = {}
        post_data['id'] = self.id
        post_data['author'] = self.author_name
        post_data['category'] = self.category
        post_data['title'] = self.title
        post_data['create_time'] = self.create_time
        post_data['update_time'] = self.update_time
        post_data['visits'] = self.visits
        return post_data
