import json

from flask import request, session, redirect, url_for
from flask_login import UserMixin
from functools import wraps
from peewee import *

from . import app


database = SqliteDatabase(app.config.get('DATABASE'))


class BaseModel(Model):
    class Meta:
        database = database


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField()
    # permission

    class Meta:
        order_by = ('username',)
    # check pwd?


class Post(BaseModel):
    user = ForeignKeyField(User) 
    author = TextField()
    title = TextField()
    content = TextField()

    class Meta:
        order_by = ('-id',)


class Magazine(BaseModel):
    title = TextField()

    class Meta:
        order_by = ('-id',)


class MagazinePost(BaseModel):
    user = ForeignKeyField(User)
    magazine = ForeignKeyField(Magazine)
    title = TextField()
    desc = TextField()
    url = CharField()
    cover = CharField()
    category = CharField()
    categoryIcon = CharField()

    class Meta:
        order_by = ('-id',)


def create_tables():
    database.connect()
    database.create_tables([User, Post, Magazine, MagazinePost])

