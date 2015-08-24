from flask import Flask

from .config import Config


app = Flask(__name__)
app.config.from_object(Config)


from .app2 import database

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


import simplecms.views.auth
import simplecms.views.post
import simplecms.views.magazine
