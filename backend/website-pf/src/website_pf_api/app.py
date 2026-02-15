from flask import Flask
from flask_cors import CORS
from markupsafe import escape
import serverless_wsgi
from website_pf_api.services import post_service
from website_pf_api.decorators.basic_request_logging import basic_request_logging


app = Flask(__name__)
CORS(app)


@app.route('/posts/recent', methods=['GET'])
@basic_request_logging
def get_recent_posts():
    return post_service.get_recent_posts()


@app.route('/posts/search', methods=['GET'])
@basic_request_logging
def search_posts():
    return post_service.search_posts()


@app.route('/posts/tags', methods=['GET'])
@basic_request_logging
def get_tags():
    return post_service.get_tags()


@app.route('/posts/tags/<tag>', methods=['GET'])
@basic_request_logging
def get_tag_posts(tag):
    return post_service.get_tag_posts(escape(tag))


@app.route('/post/<post_name>', methods=['GET'])
@basic_request_logging
def get_post(post_name):
    return post_service.get_post(escape(post_name))


def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app.app, event, context)
