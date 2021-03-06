from flask import request, render_template
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.magazine import Magazine, MagazinePost
from simplecms.utils.render import ok, error
from simplecms.utils.dump import dump_magazine_all, dump_magazine,\
    dump_magazine_post


@app.route('/api/magazines', methods=['GET'])
@login_required
def magazines():
    return ok(dump_magazine_all())


@app.route('/api/magazines/new', methods=['POST'])
@login_required
def magazines_new():
    json_data = request.get_json()

    title = json_data.get('title')

    if not all((title,)):
        return error('没有提供所有参数')

    magazine = Magazine.create_magazine(
        title=title)
    return ok(dump_magazine(magazine, mode='only_id'))


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

    json_data = request.get_json()

    title = json_data.get('title')

    if not all((title,)):
        return error('没有提供所有参数')

    magazine.update_magazine(title=title)
    return ok()


@app.route('/api/magazines/<id>/delete', methods=['POST'])
@login_required
def magazines_id_delete(id):
    try:
        magazine = Magazine.get(Magazine.id == id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    if magazine.posts.count():
        return error('杂志中有文章，确定删除请先删除杂志中的内容')

    magazine.delete_instance()
    return ok()


@app.route('/api/magazines/<mid>/posts/new', methods=['POST'])
@login_required
def magazines_mid_posts_new(mid):
    json_data = request.get_json()

    user_id = current_user.id
    magazine_id = mid
    post_id = json_data.get('post_id')
    title = json_data.get('title')
    desc = json_data.get('desc')
    cover = json_data.get('cover')
    category = json_data.get('category')
    category_icon = json_data.get('category_icon')

    if not all((magazine_id, post_id, title, cover,
               category, category_icon)):
        return error('没有提供所有参数')

    magazine_post = MagazinePost.create_magazine_post(
        user_id=user_id,
        magazine_id=magazine_id,
        post_id=post_id,
        title=title,
        desc=desc,
        cover=cover,
        category=category,
        category_icon=category_icon)
    return ok(dump_magazine_post(magazine_post, mode='only_id'))


@app.route('/api/magazines/<mid>/posts/<id>', methods=['GET'])
@login_required
def magazines_mid_posts_id(mid, id):
    try:
        magazine_post = MagazinePost.get(MagazinePost.id == id)
    except MagazinePost.DoesNotExist:
        return error('magazine_post does not exist', 404)
    return ok(dump_magazine_post(magazine_post))


@app.route('/api/magazines/<mid>/posts/<id>/update', methods=['POST'])
@login_required
def magazines_mid_posts_id_update(mid, id):
    try:
        magazine_post = MagazinePost.get(MagazinePost.id == id)
    except MagazinePost.DoesNotExist:
        return error('magazine_post does not exist', 404)

    json_data = request.get_json()

    user_id = current_user.id
    magazine_id = mid
    post_id = id

    title = json_data.get('title')
    desc = json_data.get('desc')
    cover = json_data.get('cover')
    category = json_data.get('category')
    category_icon = json_data.get('category_icon')

    if not all((magazine_id, post_id, title, desc, cover,
               category, category_icon)):
        return error('没有提供所有参数')

    magazine_post.update_magazine_post(
        user_id=user_id,
        magazine_id=magazine_id,
        post_id=post_id,
        title=title,
        desc=desc,
        cover=cover,
        category=category,
        category_icon=category_icon)
    return ok()


@app.route('/api/magazines/<mid>/posts/<id>/delete', methods=['POST'])
@login_required
def magazines_mid_posts_id_delete(mid, id):
    try:
        magazine_post = MagazinePost.get(MagazinePost.id == id)
    except MagazinePost.DoesNotExist:
        return error('magazine_post does not exist', 404)

    magazine_post.delete_instance()
    return ok()


@app.route('/magazines/<mid>', methods=['GET'])
def magazines_public(mid):
    try:
        magazine = Magazine.get(Magazine.id == mid)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    return render_template('magazine.html', magazine=dump_magazine(magazine))
