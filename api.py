from flask import Blueprint, jsonify
from datetime import datetime
import pytz
from models import db, Post, User, Favorite
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

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
        "user_id" : post.user_id,
        "created_at" : post.created_at,
        "updated_at" : post.updated_at
    } for post in posts])

# ユーザーの一覧を取得するためのapi
@api.route('/get_users', methods=['GET'])
def get_users_json():
    users = User.query.all()
    return jsonify([{
        "user_id" : user.user_id,
        "user_name" : user.user_name,
        "password" : "*" * len(user.password),
        "created_at" : user.created_at
    } for user in users])

# 画像登録のための関数
# 画像登録ができるファイルの拡張子を指定する
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

# 投稿しようとしている画像ファイルの拡張子が指定のものかどうか確認する関数
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        print('allowed_file(): 許可されていない拡張子のファイルです')
        return False

# ファイルをアップロードするための関数
def upload_file(request):
    file = request.files['file']
    if file is None:
        return None
    if file.filename == '':
        return None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None

# createのapi
@api.route('/create', methods=['POST'])
def create_post(request, user_id):
    title = request.form.get('title')
    body = request.form.get('body')
    image = upload_file(request)
    user_id = user_id
    post = Post(title=title, body=body, image=image, user_id=user_id)
    db.session.add(post)
    db.session.commit()

# updateのapi
@api.route('/update', methods=['PUT'])
def update_post(post, request):
    post.title = request.form.get('title')
    post.body = request.form.get('body')
    post.user_id = request.form.get('user_id')
    post.updated_at = datetime.now(pytz.timezone('Asia/Tokyo'))
    db.session.commit()

# deleteのapi
@api.route('/delete', methods=['DELETE'])
def delete_post(post, request):
    db.session.delete(post)
    db.session.commit()

# お気に入り機能
def check_favorite(post_id, user_id):
    stmt = (
        select(Favorite)
        .where(Favorite.post_id==post_id)
        .where(Favorite.user_id==user_id)
    )
    favorite = db.session.scalar(stmt)
    # 検索結果を返却
    return favorite

def add_favorite(favorite):
    db.session.add(favorite)
    db.session.commit()

def delete_favorite(favorite):
    db.session.delete(favorite)
    db.session.commit()
