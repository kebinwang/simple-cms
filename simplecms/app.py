import json

from flask import request, session, redirect, url_for
from functools import wraps
from peewee import *

from .init import app


DATABASE = 'simplecms-dev.db'
SECRET_KEY = 'sfserxcg8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app.config.from_object(__name__)

database = SqliteDatabase(DATABASE)


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


@app.before_request
def before_request():
    database.connect()
    # print('before')


@app.after_request
def after_request(response):
    database.close()
    # print('after')
    return response


@app.route('/index')
@app.route('/')
def index():
    return 'hello world'


@app.route('/test_add')
def test_add():
    user = User.create(
        username='un2', #request.args.get('un'),
        password='pw2' #request.args.get('pw')
    )
    return 'OK'


@app.route('/test_read')
def test_read():
    user = User.get(
        username='un'
    )
    return user.password

@app.route('/test_read_all')
def test_read_all():
    users = User.select()
    s = ''
    for user in users:
        s = s + user.username + ', '
    return s


@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.get_json()
    response = {}
    try:
        user = User.get(
            username=json_data.get('username'))
    except User.DoesNotExist:
        response['code'] = 211
        response['message'] = 'Could not find user'
    else:
        if user.password != json_data.get('password'):
            response['code'] = 210
            response['message'] = 'The username and password mismatch.'
        else:
            # response['code'] = 200
            response['username'] = user.username
            login_user(user)
    finally:
        pass
    
    return json.dumps(response)


@app.route('/api/logout', methods=['GET'])
def logout():
    logout_user()
    return 'OK'


@app.route('/api/post', methods=['POST'])
@login_required
def new_post():
    json_data = request.get_json()
    post = Post.create(
        user=session['user_id'],
        author=json_data.get('author'),
        title=json_data.get('title'),
        content=json_data.get('content'))
    response = {}
    response['err'] = 0

    return json.dumps(response)


@app.route('/api/post/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_post(id):
    response = {}
    if request.method == 'GET':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            response['author'] = post.author
            response['title'] = post.title
            response['content'] = post.content
        finally:
            pass
    elif request.method == 'PUT':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            json_data = request.get_json()
            post.author = json_data.get('author')
            post.title = json_data.get('title')
            post.content = json_data.get('content')
            post.save()
        finally:
            pass
    elif request.method == 'DELETE':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            post.delete_instance()
        finally:
            pass
    return json.dumps(response)


@app.route('/api/posts', methods=['GET'])
@login_required
def get_posts():
    response = []
    for post in Post.select():
        post_data = {}
        post_data['id'] = post.id
        post_data['author'] = post.author
        post_data['title'] = post.title
        # post_data['content'] = post.content
        response.append(post_data)
    return json.dumps(response)


@app.route('/api/magazine', methods=['GET', 'POST'])
@login_required
def magazines():
    response = []
    if request.method == 'GET':
        for magazine in Magazine.select():
            magazine_data = {}
            magazine_data['id'] = magazine.id
            magazine_data['title'] = magazine.title
            magazine_data['posts'] = []
            
            for magazine_post in MagazinePost.select().where(MagazinePost.magazine == magazine.id):
                magazine_post_data = {}
                magazine_post_data['id'] = magazine_post.id
                magazine_post_data['title'] = magazine_post.title
                magazine_post_data['desc'] = magazine_post.desc
                magazine_post_data['url'] = magazine_post.url
                magazine_post_data['cover'] = magazine_post.cover
                magazine_post_data['category'] = magazine_post.category
                magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
                magazine_data['posts'].append(magazine_post_data)
            
            response.append(magazine_data)
    elif request.method == 'POST':
        json_data = request.get_json()
        magazine = Magazine.create(
            title=json_data.get('title'))
    return json.dumps(response)


@app.route('/api/magazine/<id>', methods=['GET', 'PUT'])
@login_required
def magazine(id):
    response = {}
    if request.method == 'GET':
        try:
            magazine = Magazine.get(Magazine.id==id)
        except Magazine.DoesNotExist:
            pass
        else:
            response['id'] = magazine.id
            response['title'] = magazine.title
            response['posts'] = []

            for magazine_post in MagazinePost.select().where(MagazinePost.magazine == magazine.id):
                magazine_post_data = {}
                magazine_post_data['id'] = magazine_post.id
                magazine_post_data['title'] = magazine_post.title
                magazine_post_data['desc'] = magazine_post.desc
                magazine_post_data['url'] = magazine_post.url
                magazine_post_data['cover'] = magazine_post.cover
                magazine_post_data['category'] = magazine_post.category
                magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
                response['posts'].append(magazine_post_data)
        finally:
            pass
    elif request.method == 'PUT':
        try:
            magazine = Magazine.get(Magazine.id==id)
        except Magazine.DoesNotExist:
            pass
        else:
            # remove old post
            query = MagazinePost.delete().where(MagazinePost.magazine == id)
            query.execute()
            # and new post
            json_data = request.get_json()
            for post_data in json_data:
                MagazinePost.create(
                    user=session['user_id'],
                    magazine=id,
                    title=post_data.get('title'),
                    desc=post_data.get('desc'),
                    url=post_data.get('url'),
                    cover=post_data.get('cover'),
                    category=post_data.get('category'),
                    categoryIcon=post_data.get('categoryIcon'))
    return json.dumps(response)
