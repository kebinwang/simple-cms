import json

from flask import request, jsonify
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.post import Post
from simplecms.utils.render import ok, error, simplejsonify


@app.route('/api/post', methods=['POST'])
@login_required
def new_post():
    json_data = request.get_json()
    #TODO: 下面这样异常处理可以吗？
    try:
        post = Post.create_new(
            user=current_user.id,
            author_name=json_data.get('author'),
            title=json_data.get('title'),
            content=json_data.get('content'))
    except Exception as e:
        return error(str(e))
    return ok('successfully created')


@app.route('/api/post/<id>', methods=['GET'])
@login_required
def get_post(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        #TODO: 如果不存在的话这样处理是不是合适？
        return error('post does not exist', 404)
    post_data = {}
    post_data['author'] = post.author_name
    post_data['title'] = post.title
    post_data['content'] = post.content
    return jsonify(post_data)


@app.route('/api/post/<id>', methods=['POST'])
@login_required
def modify_post(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        #TODO: 如果不存在的话这样处理是不是合适？
        return error('post does not exist', 404)

    json_data = request.get_json()
    operation = json_data.get('operation')

    if operation == 'edit':
        new_data = json_data.get('new_data')
        try:
            post.update_post(new_data)
        except Exception as e:
            return error(str(e))
        return ok('successfully updated')
    elif operation == 'delete':
        try:
            post.delete_instance()
        except Exception as e:
            return error(str(e))
        return ok('successfully deleted')

    return error('unknown operation')


@app.route('/api/posts', methods=['GET'])
@login_required
def get_posts():
    posts_data = []
    posts = Post.get_all_posts()
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['author'] = post.author_name
        post_data['title'] = post.title
        posts_data.append(post_data)
    return simplejsonify(posts_data)
