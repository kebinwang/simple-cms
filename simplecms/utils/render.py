import json

from flask import jsonify, Response


def simplejsonify(data):
    return Response(json.dumps(data), mimetype='application/json')


def ok(res):
    return jsonify({
        'status': 'ok',
        'content': res,
    })


def error(res, status_code=400):
    return jsonify({
        'status': 'error',
        'content': res,
    }), status_code
