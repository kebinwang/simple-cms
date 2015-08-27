import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import CharField, FixedCharField, DateTimeField

from .base import BaseModel


class User(UserMixin, BaseModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    username = CharField(unique=True, max_length=60)
    password_hash = FixedCharField(max_length=128)

    @classmethod
    def create_new(username, password):
        return User.create(
            username=username,
            password=password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
