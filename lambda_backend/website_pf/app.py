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


@app.route('/home', methods=['GET'])
@basic_request_logging
def home():
    return post_service.get_recent_posts()


@app.route('/post/<post_name>', methods=['GET'])
@basic_request_logging
def post(post_name):
    return post_service.get_post(escape(post_name))


@app.route('/search', methods=['GET'])
@basic_request_logging
def search():
    return post_service.search_posts()


@app.route('/tags', methods=['POST'])
@basic_request_logging
def tags():
    return 'tags !'
