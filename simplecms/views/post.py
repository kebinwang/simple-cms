from flask_login import login_required, current_user

from simplecms import app
from simplecms.app2 import *


@app.route('/api/post', methods=['POST'])
@login_required
def new_post():
    json_data = request.get_json()
    post = Post.create(
        user=current_user.id,
        author=json_data.get('author'),
        title=json_data.get('title'),
        content=json_data.get('content'))
    response = {}
    response['err'] = 0

    return json.dumps(response)


@app.route('/api/post/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_post(id):
    response = {}
    if request.method == 'GET':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            response['author'] = post.author
            response['title'] = post.title
            response['content'] = post.content
        finally:
            pass
    elif request.method == 'PUT':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            json_data = request.get_json()
            post.author = json_data.get('author')
            post.title = json_data.get('title')
            post.content = json_data.get('content')
            post.save()
        finally:
            pass
    elif request.method == 'DELETE':
        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            pass
        else:
            post.delete_instance()
        finally:
            pass
    return json.dumps(response)


@app.route('/api/posts', methods=['GET'])
@login_required
def get_posts():
    response = []
    for post in Post.select():
        post_data = {}
        post_data['id'] = post.id
        post_data['author'] = post.author
        post_data['title'] = post.title
        # post_data['content'] = post.content
        response.append(post_data)
    return json.dumps(response)
