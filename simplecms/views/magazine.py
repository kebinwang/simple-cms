from flask_login import login_required, current_user

from simplecms import app
from simplecms.app2 import *

@app.route('/api/magazine', methods=['GET', 'POST'])
@login_required
def magazines():
    response = []
    if request.method == 'GET':
        for magazine in Magazine.select():
            magazine_data = {}
            magazine_data['id'] = magazine.id
            magazine_data['title'] = magazine.title
            magazine_data['posts'] = []
            
            for magazine_post in MagazinePost.select().where(MagazinePost.magazine == magazine.id):
                magazine_post_data = {}
                magazine_post_data['id'] = magazine_post.id
                magazine_post_data['title'] = magazine_post.title
                magazine_post_data['desc'] = magazine_post.desc
                magazine_post_data['url'] = magazine_post.url
                magazine_post_data['cover'] = magazine_post.cover
                magazine_post_data['category'] = magazine_post.category
                magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
                magazine_data['posts'].append(magazine_post_data)
            
            response.append(magazine_data)
    elif request.method == 'POST':
        json_data = request.get_json()
        magazine = Magazine.create(
            title=json_data.get('title'))
    return json.dumps(response)


@app.route('/api/magazine/<id>', methods=['GET', 'PUT'])
@login_required
def magazine(id):
    response = {}
    if request.method == 'GET':
        try:
            magazine = Magazine.get(Magazine.id==id)
        except Magazine.DoesNotExist:
            pass
        else:
            response['id'] = magazine.id
            response['title'] = magazine.title
            response['posts'] = []

            for magazine_post in MagazinePost.select().where(MagazinePost.magazine == magazine.id):
                magazine_post_data = {}
                magazine_post_data['id'] = magazine_post.id
                magazine_post_data['title'] = magazine_post.title
                magazine_post_data['desc'] = magazine_post.desc
                magazine_post_data['url'] = magazine_post.url
                magazine_post_data['cover'] = magazine_post.cover
                magazine_post_data['category'] = magazine_post.category
                magazine_post_data['categoryIcon'] = magazine_post.categoryIcon
                response['posts'].append(magazine_post_data)
        finally:
            pass
    elif request.method == 'PUT':
        try:
            magazine = Magazine.get(Magazine.id==id)
        except Magazine.DoesNotExist:
            pass
        else:
            # remove old post
            query = MagazinePost.delete().where(MagazinePost.magazine == id)
            query.execute()
            # and new post
            json_data = request.get_json()
            for post_data in json_data:
                MagazinePost.create(
                    user=current_user,
                    magazine=id,
                    title=post_data.get('title'),
                    desc=post_data.get('desc'),
                    url=post_data.get('url'),
                    cover=post_data.get('cover'),
                    category=post_data.get('category'),
                    categoryIcon=post_data.get('categoryIcon'))
    return json.dumps(response)
