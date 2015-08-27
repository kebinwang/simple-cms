import json
from flask import request
from flask_login import login_required, login_user, logout_user

from simplecms import app
from simplecms.models.user import User
from simplecms.utils.render import ok, error


@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.get_json()
    response = {}
    try:
        user = User.get(
            username=json_data.get('username'))
    except User.DoesNotExist:
        return error((211, 'Could not find user'))
    if not user.verify_password(json_data.get('password')):
        return error((210, 'The username and password mismatch.'))
    login_user(user)
    return ok({'username': user.username, 'user_id': user.id})


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return ok()
