# Python Flask App

from flask import Flask
from services import post_service

app = Flask(__name__)

@app.route('/home', methods = ['GET'])
def home():
    return post_service.getRecentPosts()

@app.route('/post/*', methods = ['GET'])
def post():
    return 'post !'

@app.route('/search', methods = ['POST'])
def search():
    return 'search !'

@app.route('/tags', methods = ['POST'])
def tags():
    return 'tags !'