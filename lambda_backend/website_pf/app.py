# Python Flask App
from flask import Flask
from flask_cors import CORS
from markupsafe import escape
from src.services import post_service
from src.decorators.basic_request_logging import basic_request_logging
import config


app = Flask(__name__)
CORS(app)
app.logger.setLevel(config.LOG_LEVEL)


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
