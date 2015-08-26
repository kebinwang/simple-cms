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
    def get_all_posts(self):
        return list(Post.select())

    def update_post(self, new_data):
        self.author_name = new_data.get('author')
        self.title = new_data.get('title')
        self.content = new_data.get('content')
        self.save()
