from flask import Blueprint, jsonify
from datetime import datetime
import pytz
from models import db, Post

api = Blueprint('api', __name__)

def init_api(app):
    # 「url_prefix='/api'」の記述により、apiのURLは/api始まりで統一する
    app.register_blueprint(api, url_prefix='/api')

# 投稿の一覧を取得するためのapi
@api.route('/get_posts', methods=['GET'])
def get_posts_json():
    posts = Post.query.all()
    return jsonify([{
        "post_id" : post.post_id,
        "title" : post.title,
        "body" : post.body,
        "url" : post.url,
        "created_at" : post.created_at,
        "updated_at" : post.updated_at
    } for post in posts])

# createのapi
@api.route('/create', methods=['POST'])
def create_post(request):
    title = request.form.get('title')
    body = request.form.get('body')
    url = request.form.get('url')
    post = Post(title=title, body=body, url=url)
    db.session.add(post)
    db.session.commit()

# updateのapi
@api.route('/update', methods=['PUT'])
def update_post(post, request):
    post.title = request.form.get('title')
    post.body = request.form.get('body')
    post.url = request.form.get('url')
    post.updated_at = datetime.now(pytz.timezone('Asia/Tokyo'))
    db.session.commit()

# deleteのapi
@api.route('/delete', methods=['DELETE'])
def delete_post(post, request):
    db.session.delete(post)
    db.session.commit()