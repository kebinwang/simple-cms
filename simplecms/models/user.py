import datetime

from flask_login import UserMixin
from peewee import CharField, DateTimeField

from .base import BaseModel


class User(UserMixin, BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    username = CharField(unique=True, max_length=60)
    password = CharField(max_length=60)

    class Meta:
        pass

    @classmethod
    def create_new(username, password):
        return User.create(
            username=username,
            password=password)
