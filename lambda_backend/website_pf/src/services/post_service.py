# Post Services
from src.repositories import mysql_repository
from flask import Response
from flask import request
import config
import logging
from src.utils import utils
from src.models.post import Post

logger = logging.getLogger('app.services.post_service')
logger.setLevel(config.LOG_LEVEL)


def get_recent_posts():
    try:
        query = 'SELECT post_name, post_url, primary_image_path FROM post order by created_date desc limit 5'
        params = ()
        data = mysql_repository.mysql_select(query, params)
        records = format_posts_response(data)
        return Response(response=utils.serialize_reponse(records), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def search_posts():
    try:
        query = 'SELECT p.post_name, p.post_url, p.primary_image_path, p.post_summary, p.created_date, p.updated_date, a.display_name \
        FROM post p \
        INNER JOIN author a on p.author_id=a.id \
        where p.post_name like %s order by created_date desc limit 1000'
        params = [(f'%{request.args["q"]}%')]
        data = mysql_repository.mysql_select(query, params)
        records = format_posts_response(data)
        return Response(response=utils.serialize_reponse({'posts': records}), status=200, mimetype='application/json')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return Response(response=utils.serialize_reponse({}), status=500, mimetype='application/json')


def get_post(post_name):
    try:
        sql = 'SELECT p.post_name, p.post_url, p.primary_image_path, p.post_html_path, ' \
            ' p.post_summary, p.created_date, p.updated_date, ' \
            ' a.username, a.display_name FROM post p ' \
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
    logger.debug(data)
    for d in data:
        p = Post()
        p.post_name = d[0]
        p.post_url = '/post/' + d[1]
        p.primary_image_path = utils.get_s3_public_url(config.WEBSITE_URL, d[2])
        p.post_html = '  '
        p.post_summary = d[3]
        p.post_created_date = d[4]
        p.post_updated_date = d[5]
        p.author_username = ' '
        p.author_name = d[6]

        posts.append(p)
    return posts


def format_single_post_response(data) -> Post:
    p = Post()
    if (data and len(data) > 0):
        logger.debug(data)
        d = data[0]
        p.post_name = d[0]
        p.post_url = '/post/' + d[1]
        p.post_slug = d[1]
        p.primary_image_path = utils.get_s3_public_url(config.WEBSITE_URL, d[2])
        p.post_html = utils.get_s3_object(d[3])
        p.post_summary = d[4]
        p.post_created_date = d[5]
        p.post_updated_date = d[6]
        p.author_username = d[7]
        p.author_name = d[8]
    return p
