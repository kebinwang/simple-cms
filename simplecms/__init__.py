from flask import Flask, session
from flask_login import LoginManager
from peewee import SqliteDatabase, MySQLDatabase
from playhouse.db_url import connect

from .config import Config


app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

database = connect(app.config.get('MYSQL_DB_URL') or 'sqlite:///default.db')


from simplecms.models.user import User


@login_manager.user_loader
def load_user(userid):
    return User.get(User.id == userid)


@app.route('/index')
@app.route('/')
def index():
    return 'hello'


import simplecms.views.auth
import simplecms.views.post
import simplecms.views.magazine
