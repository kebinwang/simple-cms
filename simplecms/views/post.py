from flask import request, render_template
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.post import Post
from simplecms.utils.render import ok, error
from simplecms.utils.dump import dump_post_list, dump_post


@app.route('/api/posts/new', methods=['POST'])
@login_required
def posts_new():
    json_data = request.get_json()
    user_id = current_user.id
    author_name = json_data.get('author')
    category = json_data.get('category')
    title = json_data.get('title')
    content = json_data.get('content')

    if not all((author_name, category, title, content)):
        return error('没有提供所有参数')

    post = Post.create_post(
        user_id=user_id,
        author_name=author_name,
        category=category,
        title=title,
        content=content)
    return ok(dump_post(post, mode='only_id'))


@app.route('/api/posts/<id>', methods=['GET'])
@login_required
def posts_id(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)
    # post.update_visits()
    return ok(dump_post(post))


@app.route('/api/posts/<id>/update', methods=['POST'])
@login_required
def posts_id_update(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)

    json_data = request.get_json()

    author_name = json_data.get('author')
    category = json_data.get('category')
    title = json_data.get('title')
    content = json_data.get('content')

    if not all((author_name, category, title, content)):
        return error('没有提供所有参数')

    post.update_post(
        author_name=author_name,
        category=category,
        title=title,
        content=content)
    return ok()


@app.route('/api/posts/<id>/delete', methods=['POST'])
@login_required
def posts_id_delete(id):
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)

    if post.magazine_posts.count():
        return error('存在关联的杂志引用，确定删除需要先删除关联的杂志引用')

    post.delete_instance()
    return ok()

@app.route('/api/posts', methods=['GET'])
@login_required
def posts():
    return ok(dump_post_list())


@app.route('/posts/<id>', methods=['GET'])
def posts_public(id):

    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        return error('post does not exist', 404)

    post.update_visits()
    return render_template('posts.html', post=post)

@app.route('/god', methods=['GET'])
def god():
    return render_template('god.html')
