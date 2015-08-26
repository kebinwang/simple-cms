import json
from flask import request, jsonify
from flask_login import login_required, current_user

from simplecms import app
from simplecms.models.magazine import Magazine, MagazinePost
from simplecms.utils.render import ok, error, simplejsonify


@app.route('/api/magazines', methods=['GET'])
@login_required
def magazines():
    magazines = Magazine.get_all_magazines()
    magazines_data = []
    for magazine in magazines:
        magazine_data = {}
        magazine_data['id'] = magazine.id
        magazine_data['title'] = magazine.title
        magazine_data['posts'] = []

        magazine_posts = MagazinePost.get_post_with_magazine_id(magazine.id)
        for magazine_post in magazine_posts:
            magazine_post_data = {}
            magazine_post_data['id'] = magazine_post.id
            magazine_post_data['title'] = magazine_post.title
            magazine_post_data['desc'] = magazine_post.desc
            magazine_post_data['url'] = magazine_post.url
            magazine_post_data['cover'] = magazine_post.cover
            magazine_post_data['category'] = magazine_post.category
            magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
            magazine_data['posts'].append(magazine_post_data)
        magazines_data.append(magazine_data)
    return ok(magazines_data)


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
        magazine = Magazine.get(Magazine.id==id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    magazine_data = {}
    magazine_data['id'] = magazine.id
    magazine_data['title'] = magazine.title
    magazine_data['posts'] = []

    magazine_posts = MagazinePost.get_post_with_magazine_id(magazine.id)
    for magazine_post in magazine_posts:
        magazine_post_data = {}
        magazine_post_data['id'] = magazine_post.id
        magazine_post_data['title'] = magazine_post.title
        magazine_post_data['desc'] = magazine_post.desc
        magazine_post_data['url'] = magazine_post.url
        magazine_post_data['cover'] = magazine_post.cover
        magazine_post_data['category'] = magazine_post.category
        magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
        magazine_data['posts'].append(magazine_post_data)

    return ok(magazine_data)


@app.route('/api/magazines/<id>/update', methods=['POST'])
@login_required
def magazines_id_update(id):
    #TODO: 是否需要单独去处理每一条 magazine 的 post，Magazine 的组成有待确认
    try:
        magazine = Magazine.get(Magazine.id==id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    new_data = request.get_json()
    # remove old post
    query = MagazinePost.delete().where(MagazinePost.magazine == id)
    query.execute()
    # and new post
    for post_data in new_data:
        MagazinePost.create_new(
            user=current_user.id,
            magazine=id,
            title=post_data.get('title'),
            desc=post_data.get('desc'),
            url=post_data.get('url'),
            cover=post_data.get('cover'),
            category=post_data.get('category'),
            categoryIcon=post_data.get('categoryIcon'))
    return ok()


@app.route('/api/magazines/<id>/delete', methods=['POST'])
@login_required
def magazines_id_delete(id):
    try:
        magazine = Magazine.get(Magazine.id==id)
    except Magazine.DoesNotExist:
        return error('magazine does not exist', 404)

    magazine.delete_instance()
    return ok()
