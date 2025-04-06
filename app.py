from flask import Flask, url_for
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from api import create_post, update_post, delete_post, check_favorite, add_favorite, delete_favorite
from personalinfo import UPLOARD_FOLDER, SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devicesquare.db'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOARD_FOLDER'] = UPLOARD_FOLDER

# dbをmodels.pyに外だししたためインポート
from models import db, Post, User, Favorite
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

# apiを利用できるようにするためのインポート
from api import init_api
init_api(app)

# ログイン状態を管理するための関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ユーザー登録画面を表示するためのルーティング
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User(user_name=user_name,
                    password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('/signup.html')

# ログイン画面を表示するためのルーティング
@app.route('/login', methods=['GET', 'POST'])
def login():
    text = None
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter_by(user_name=user_name).first()
        if user is None:
            text = 'ユーザーが登録されていません'
            return render_template('/login.html', text=text)
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            elif check_password_hash(user.password, password) is False:
                text = 'パスワードが違います'
                return render_template('/login.html', text=text)
    else:
        return render_template('/login.html', text=text)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

# 初期画面表示のためのルーティング
@app.route('/', methods=['GET', 'POST'])
# @login_required
def homepage():
    posts = Post.query.all()
    return render_template('homepage.html', posts=posts)

# 投稿作成画面表示のためのルーティング
@app.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    if request.method == 'POST':
        create_post(request, current_user.user_id)
        return redirect('/')
    else:
        return render_template('create.html')

# 投稿更新画面表示のためのルーティング
@app.route('/<int:post_id>/update', methods=['GET', 'POST'])
# @login_required
def update(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        update_post(post, request)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('update.html', post=post)

# 投稿を削除するためのルーティング
@app.route('/<int:post_id>/delete', methods=['GET', 'POST'])
# @login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        delete_post(post, request)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('delete.html', post=post)

# 投稿の詳細画面を表示するためのルーティング
@app.route('/<int:post_id>/detail/<string:title>', methods=['GET'])
# @login_required
def post_detail(post_id, title):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post, check_favorite=check_favorite(post_id, current_user.user_id))

# 投稿に対してお気に入り機能を使うためのルーティング
@app.route('/<int:post_id>/favorite', methods=['GET'])
# @login_required
def favorite(post_id):
    favorite = check_favorite(post_id, current_user.user_id)
    # 検索結果がある（favoriteテーブルに登録されている）場合は削除、ない（テーブル未登録）の場合は追加
    if favorite:
        delete_favorite(favorite)
        post = Post.query.get(post_id)
        return redirect(url_for('post_detail', post_id=post_id, title=post.title))
    else:
        favorite = Favorite(post_id=post_id, user_id=current_user.user_id)
        add_favorite(favorite)
        post = Post.query.get(post_id)
        return redirect(url_for('post_detail', post_id=post_id, title=post.title))
