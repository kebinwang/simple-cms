import json

from flask import request, session, redirect, url_for
from functools import wraps
from peewee import *

from . import app


database = SqliteDatabase(app.config.get('DATABASE'))


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
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


def login_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username


def logout_user():
    session['logged_in'] = False
    session.pop('user_id')
    session.pop('username')


def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner
