# Post Services
# from website_pf_post_loader.repositories import mysql_repository as mysql
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
import xml.etree.cElementTree as ET
import boto3
import os
import datetime
import logging
from website_pf_post_loader import config
from website_pf_post_loader.utils import utils

logger = logging.getLogger()
utils.setup_logging(logger)
s3_resource = boto3.resource('s3')


def generate_robots():
    try:
        data = '''User-agent: *\n
                Allow: /\n
                Sitemap: ''' + config.WEBSITE_URL + 'sitemap.xml\n'
        _put_file_website_bucket('robots.txt', data, 'maxage=86400,s-maxage=86400', 'text/plain')
        return True
    except Exception:
        logger.error('Could not generate robots.txt file', exc_info=True)
    return False


def generate_rss():
    try:
        rss = ET.Element('rss', attrib={'version': '2.0'})
        channel = ET.SubElement(rss, 'channel')
        title = ET.SubElement(channel, 'title', attrib={})
        title.text = config.WEBSITE_URL
        link = ET.SubElement(channel, 'link', attrib={})
        link.text = config.WEBSITE_URL
        description = ET.SubElement(channel, 'description', attrib={})
        description.text = 'A tech blog and portfolio'

        _xml_build_rss_item(channel, 'Sitemap', f'{config.WEBSITE_URL}/sitemap.xml', 'Website sitemap')
        # build other rss items here
        data = ET.tostring(rss, encoding='utf8', method='xml')
        _put_file_website_bucket('rss.xml', data, 'maxage=0,s-maxage=0', 'application/xml')
        return True
    except Exception:
        logger.error('Could not generate rss.xml file', exc_info=True)
    return False


def generate_sitemap():
    try:
        sitemap = ET.Element('urlset', attrib={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})

        date_now = datetime.datetime.now().strftime("%Y-%m-%d")
        _xml_build_sitemap_url(sitemap, 'https://prestonfrazier.net/', date_now, 'monthly', '1.0')
        _xml_build_sitemap_url(sitemap, 'https://prestonfrazier.net/about', date_now, 'monthly', '1.0')
        # build other sitemap urls here
        data = ET.tostring(sitemap, encoding='utf8', method='xml')
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
    config_obj = s3_resource.Object(config.S3_WEBSITE_PF_BUCKET, s3_key)
    config_obj.put(Body=data, ContentType=content_type, CacheControl=cache_control)


def _xml_build_rss_item(node, p_title, p_link, p_description):
    item = ET.SubElement(node, 'item', attrib={})

    title = ET.SubElement(item, 'title', attrib={})
    title.text = p_title
    link = ET.SubElement(item, 'link', attrib={})
    link.text = p_link
    description = ET.SubElement(item, 'description', attrib={})
    description.text = p_description


def _xml_build_sitemap_url(node, p_url, p_last_modified, p_change_frequency, p_priority):
    url = ET.SubElement(node, 'url', attrib={})

    loc = ET.SubElement(url, 'loc', attrib={})
    loc.text = p_url
    lastmod = ET.SubElement(url, 'lastmod', attrib={})
    lastmod.text = p_last_modified
    changefreq = ET.SubElement(url, 'changefreq', attrib={})
    changefreq.text = p_change_frequency
    priority = ET.SubElement(url, 'priority', attrib={})
    priority.text = p_priority
