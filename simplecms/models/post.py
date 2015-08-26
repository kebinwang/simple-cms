from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .user import User

class Post(BaseModel):
    user = ForeignKeyField(User) 
    author_name = CharField(max_length=60)
    title = CharField(max_length=120)
    content = TextField()

    #TODO: Meta 用来做什么，order_by 有没有用？
    class Meta:
        order_by = ('-id',)

    @classmethod
    def create_new(self, user, author_name, title, content):
        return Post.create(
            user=user,
            author_name=author_name,
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
        self.title = new_data.get('title')
        self.content = new_data.get('content')
        self.save()

    def dump(self):
        post_data = {}
        post_data['author'] = self.author_name
        post_data['title'] = self.title
        post_data['content'] = self.content
        return post_data

    def dump_desc(self):
        post_data = {}
        post_data['id'] = self.id
        post_data['author'] = self.author_name
        post_data['title'] = self.title
        return post_data
