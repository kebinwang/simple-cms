import json
from flask import request
from flask_login import login_required, login_user, logout_user

from simplecms import app
from simplecms.app2 import *


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
@login_required
def logout():
    logout_user()
    return 'OK'
