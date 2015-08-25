from flask_login import UserMixin
from peewee import CharField

from .base import BaseModel


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        order_by = ('username',)

    @classmethod
    def create_new(username, password):
        return User.create(
            username=username,
            password=password)
