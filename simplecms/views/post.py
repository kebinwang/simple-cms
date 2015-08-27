from flask import request
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.post import Post
from simplecms.utils.render import ok, error
from simplecms.utils.dump import dump_post_list, dump_post


@app.route('/api/posts/new', methods=['POST'])
@login_required
def posts_new():
    json_data = request.get_json()
    Post.create_new(
        user=current_user.id,
        author_name=json_data.get('author'),
        category=json_data.get('category'),
        title=json_data.get('title'),
        content=json_data.get('content'))
    return ok()


@app.route('/api/posts/<id>', methods=['GET'])
@login_required
def posts_id(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)
    return ok(dump_post(post))


@app.route('/api/posts/<id>/update', methods=['POST'])
@login_required
def posts_id_update(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)

    new_data = request.get_json()

    post.update_post(new_data)
    return ok()


@app.route('/api/posts/<id>/delete', methods=['POST'])
@login_required
def posts_id_delete(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)

    post.delete_instance()
    return ok()


@app.route('/api/posts', methods=['GET'])
@login_required
def posts():
    return ok(dump_post_list())
