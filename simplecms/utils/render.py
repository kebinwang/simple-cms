import json

from flask import jsonify, Response


def simplejsonify(data):
    return Response(json.dumps(data), mimetype='application/json')


def ok(content=''):
    msg = {
        'status': 'ok',
        'content': content,
    }

    resp = jsonify(msg)
    return resp


def error(error='', status_code=400):
    if isinstance(error, (tuple, list)):
        msg = {
            'status': 'error',
            'code': error[0],
            'msg': error[1],
        }
    else:
        msg = {
            'status': 'error',
            'msg': error,
        }

    resp = jsonify(msg, status_code=status_code)
    return resp
