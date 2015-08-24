from peewee import TextField, ForeignKeyField

from .base import BaseModel
from .user import User

class Post(BaseModel):
    user = ForeignKeyField(User) 
    author = TextField()
    title = TextField()
    content = TextField()

    class Meta:
        order_by = ('-id',)
