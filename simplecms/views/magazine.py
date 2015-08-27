from flask import request
from flask_login import login_required

from simplecms import app
from simplecms.models.magazine import Magazine
from simplecms.utils.render import ok, error
from simplecms.utils.dump import dump_magazine_all, dump_magazine


@app.route('/api/magazines', methods=['GET'])
@login_required
def magazines():
    return ok(dump_magazine_all())


@app.route('/api/magazines/new', methods=['POST'])
@login_required
def magazines_new():
    json_data = request.get_json()
    Magazine.create_new(
        title=json_data.get('title'))
    return ok()


@app.route('/api/magazines/<id>', methods=['GET'])
@login_required
def magazines_id(id):
    try:
        magazine = Magazine.get(Magazine.id == id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)
    return ok(dump_magazine(magazine))


@app.route('/api/magazines/<id>/update', methods=['POST'])
@login_required
def magazines_id_update(id):
    try:
        magazine = Magazine.get(Magazine.id == id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    new_data = request.get_json()
    magazine.update_posts(new_data)
    return ok()


@app.route('/api/magazines/<id>/delete', methods=['POST'])
@login_required
def magazines_id_delete(id):
    try:
        magazine = Magazine.get(Magazine.id == id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    magazine.delete_instance()
    return ok()
