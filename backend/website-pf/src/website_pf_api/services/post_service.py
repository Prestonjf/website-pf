# Post Services
from flask import Response
from flask import request
import logging
import json
from website_pf_api.repositories import mysql_repository
from website_pf_api.utils import utils
from website_pf_api.models.post import Post
from website_pf_api.models.author import Author

logger = logging.getLogger()
utils.setup_logging(logger)


def get_recent_posts():
    try:
        query = 'SELECT p.post_name, p.post_url, p.thumbnail_image_path, p.post_summary, p.created_date, p.updated_date, a.display_name, p.meta \
        FROM post p \
        INNER JOIN author a on p.author_id=a.id \
        order by p.created_date desc limit 5'
        params = []
        data = mysql_repository.mysql_select(query, params)
        records = format_posts_response(data)
        return Response(response=utils.serialize_reponse({'posts': records}), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def search_posts():
    try:
        query = 'SELECT p.post_name, p.post_url, p.thumbnail_image_path, p.post_summary, p.created_date, p.updated_date, a.display_name, p.meta \
        FROM post p \
        INNER JOIN author a on p.author_id=a.id \
        where p.post_name like %s order by p.created_date desc '
        params = [(f'%{request.args["q"]}%')]
        data = mysql_repository.mysql_select(query, params)
        records = format_posts_response(data)
        return Response(response=utils.serialize_reponse({'posts': records}), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def get_tag_posts(tag):
    try:
        query = 'SELECT p.post_name, p.post_url, p.thumbnail_image_path, p.post_summary, p.created_date, p.updated_date, a.display_name, p.meta \
        FROM post p \
        INNER JOIN author a on p.author_id=a.id \
        where JSON_SEARCH(meta->"$.tags", "one", %s) is not null order by p.created_date desc '
        params = [(tag)]
        data = mysql_repository.mysql_select(query, params)
        records = format_posts_response(data)
        return Response(response=utils.serialize_reponse({'posts': records}), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def get_tags():
    try:
        query = 'SELECT p.meta FROM post p'
        params = []
        data = mysql_repository.mysql_select(query, params)
        tags = get_tags_from_posts(data)
        return Response(response=utils.serialize_reponse({'tags': tags}), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving tags', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def get_post(post_name):
    try:
        sql = 'SELECT p.post_name, p.post_url, p.thumbnail_image_path, p.post_html_path, ' \
            ' p.post_summary, p.created_date, p.updated_date, ' \
            ' a.username, a.display_name, p.meta FROM post p ' \
            ' inner join author a on a.id=p.author_id where p.post_url=%s '
        params = [(post_name)]
        logger.info('querying mysql')
        data = mysql_repository.mysql_select(sql, params)
        record: Post = format_single_post_response(data)
        return Response(response=utils.serialize_reponse(record), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def format_posts_response(data):
    posts = []
    for d in data:
        p = Post()
        p.name = d[0]
        p.id = d[1]
        p.primaryImageFile = d[2]
        p.primaryImageThumbnail = d[2]
        p.htmlFile = ''
        p.summary = d[3]
        p.createdDate = d[4]
        p.updatedDate = d[5]
        p.tags = json.loads(d[7])['tags']
        a = Author()
        a.name = d[6]
        p.author = a
        posts.append(p)
    return posts


def format_single_post_response(data) -> Post:
    p = Post()
    if (data and len(data) > 0):
        d = data[0]
        p.name = d[0]
        p.id = d[1]
        p.idName = d[1]
        p.primaryImageFile = d[2]
        p.primaryImageThumbnail = d[2]
        p.htmlFile = d[3]
        p.summary = d[4]
        p.createdDate = d[5]
        p.updatedDate = d[6]
        p.tags = json.loads(d[9])['tags']
        a = Author()
        a.username = d[7]
        a.name = d[8]
        p.author = a
    return p


def get_tags_from_posts(data):
    tags = {}
    if (data and len(data) > 0):
        for post in data:
            meta = json.loads(post[0])
            if meta['tags'] and len(meta['tags']) > 0:
                for t in meta['tags']:
                    if t in tags:
                        tags[t] += 1
                    else:
                        tags[t] = 1
    logger.debug(tags)
    return tags
