from flask import Blueprint, jsonify
from models import db, Post

api = Blueprint('api', __name__)

@api.route('/api/get', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        "post_id" : post.post_id,
        "title" : post.title,
        "body" : post.body,
        "url" : post.url,
        "created_at" : post.created_at,
        "updated_at" : post.updated_at
    } for post in posts])

def init_api(app):
    app.register_blueprint(api)