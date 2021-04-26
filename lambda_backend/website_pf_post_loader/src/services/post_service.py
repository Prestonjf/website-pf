# Post Services
# from lambda_backend.website_pf_post_loader.src.repositories import mysql_repository as mysql
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
# import xml.etree.cElementTree as ET
import boto3
import os
from lambda_backend.website_pf_post_loader.src.utils import config
import logging

logger = logging.getLogger('app.services.post_service')
logger.setLevel(config.LOG_LEVEL)
s3_resource = boto3.resource('s3')


def generate_robots():
    try:
        data = '''User-agent: *\n
                Allow: /\n
                Sitemap: ''' + os.environ['WEBSITE_URL'] + 'sitemap.xml\n'
        _put_file_website_bucket('robots.txt', data, 'maxage=86400,s-maxage=86400', 'text/plain')
        return True
    except Exception:
        logger.error('Could not generate robots.txt file', exc_info=True)
    return False


def generate_rss():
    try:
        data = ''
        _put_file_website_bucket('rss.xml', data, 'maxage=0,s-maxage=0', 'application/xml')
        return True
    except Exception:
        logger.error('Could not generate rss.xml file', exc_info=True)
    return False


def generate_sitemap():
    try:
        data = ''
        _put_file_website_bucket('sitemap.xml', data, 'maxage=0,s-maxage=0', 'application/xml')
        return True
    except Exception:
        logger.error('Could not generate sitemap.xml file', exc_info=True)
    return False


def generate_featured():
    try:
        posts = os.environ['FEATURED_POSTS'].split(',')
        featured = []
        for p in posts:
            featured.append(p)
        data = {'featured': featured}
        yaml = YAML(typ='safe')
        stream = StringIO()
        yaml.dump(data, stream)
        _put_file_website_bucket('featured.yml', stream.getvalue().encode(), 'maxage=0,s-maxage=0', 'text/yaml')
        return True
    except Exception:
        logger.error('Could not generate featured.yml file', exc_info=True)
    return False


def _put_file_website_bucket(s3_key, data, cache_control, content_type):
    config_obj = s3_resource.Object(os.environ['S3_WEBSITE_PF_BUCKET'], s3_key)
    config_obj.put(Body=data, ContentType=content_type, CacheControl=cache_control)
