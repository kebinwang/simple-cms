import json

from flask import request, jsonify
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.post import Post
from simplecms.utils.render import ok, error, simplejsonify


@app.route('/api/posts/new', methods=['POST'])
@login_required
def posts_new():
    json_data = request.get_json()
    post = Post.create_new(
        user=current_user.id,
        author_name=json_data.get('author'),
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
    post_data = {}
    post_data['author'] = post.author_name
    post_data['title'] = post.title
    post_data['content'] = post.content
    return ok(post_data)


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
    posts_data = []
    posts = Post.get_all_posts()
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['author'] = post.author_name
        post_data['title'] = post.title
        posts_data.append(post_data)
    return ok(posts_data)
