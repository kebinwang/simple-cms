from flask import Flask, session
from flask_login import LoginManager

from .config import Config


app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)


from .app2 import database, User


@app.before_request
def before_request():
    database.connect()
    # print('before')


@app.after_request
def after_request(response):
    database.close()
    # print('after')
    return response


@login_manager.user_loader
def load_user(userid):
    return User.get(User.id == userid)


@app.route('/index')
@app.route('/')
def index():
    return 'hello world'


import simplecms.views.auth
import simplecms.views.post
import simplecms.views.magazine
