from simplecms.models.post import Post
from simplecms.models.magazine import Magazine


def dump_user(user):
    r = {}
    if user:
        r['id'] = user.id
        r['username'] = user.username
    return r


def dump_post_list():
    posts_data = []
    posts = Post.all()
    for post in posts:
        posts_data.append(dump_post(post, mode='without_content'))
    return posts_data


def dump_post(post, mode='full'):
    r = {}
    if post:
        r['id'] = post.id
        if mode == 'only_id':
            return r
        r['author'] = post.author_name
        r['category'] = post.category
        r['title'] = post.title
        r['create_time'] = post.create_time
        r['update_time'] = post.update_time
        if mode == 'without_content':
            return r
        r['content'] = post.content
    return r


def dump_magazine_all():
    magazines_data = []
    magazines = Magazine.all()
    for magazine in magazines:
        magazines_data.append(dump_magazine(magazine))
    return magazines_data


def dump_magazine(magazine, mode='full'):
    r = {}
    if magazine:
        r['id'] = magazine.id
        if mode == 'only_id':
            return r
        r['title'] = magazine.title
        r['posts'] = []
        r['create_time'] = magazine.create_time
        r['update_time'] = magazine.update_time

        magazine_posts = magazine.posts
        for magazine_post in magazine_posts:
            r['posts'].append(dump_magazine_post(magazine_post))
    return r


def dump_magazine_post(magazine_post, mode='full'):
    r = {}
    if magazine_post:
        r['id'] = magazine_post.id
        if mode == 'only_id':
            return r
        r['magazine_id'] = magazine_post.magazine.id
        r['post_id'] = magazine_post.post.id
        r['title'] = magazine_post.title
        r['desc'] = magazine_post.desc
        r['cover'] = magazine_post.cover
        r['category'] = magazine_post.category
        r['category_icon'] = magazine_post.category_icon
        r['create_time'] = magazine_post.create_time
        r['update_time'] = magazine_post.update_time
    return r
