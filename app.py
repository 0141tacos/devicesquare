from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
import os
# apiを利用できるようにするためのインポート
from api import init_api
# dbをmodels.pyに外だししたためインポート
from models import db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devicesquare.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

init_api(app)

# うまく動いたら削除する
""""
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(400))
    # 画像のカラムを作りたい
    # いったん保留（画像の保管方法をDBにするか外部ストレージにするか決められないため）
    # image = db.Column(db.blob)
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # 論理削除フラグ
    # 20250227時点ではCRUDの勉強のため利用しないこととする
    delete_flag = db.Column(db.Boolean, nullable=False, default=0)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(12))
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # Flask-Loginでは"id"を定義しないといけないが、"user_id"としてしまったのでget_id()をオーバーライドしている
    def get_id(self):
        return str(self.user_id)
"""

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
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter_by(user_name=user_name).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

# 初期画面表示のためのルーティング
@app.route('/', methods=['GET', 'POST'])
def homepage():
    posts = Post.query.all()
    return render_template('homepage.html', posts=posts)

# 投稿作成画面表示のためのルーティング
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        url = request.form.get('url')
        post = Post(title=title, body=body, url=url)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

# 投稿更新画面表示のためのルーティング
@app.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        post.url = request.form.get('url')
        post.updated_at = datetime.now(pytz.timezone('Asia/Tokyo'))
        db.session.commit()
        return redirect('/')
    elif request.method == 'GET':
        return render_template('update.html', post=post)

# 投稿を削除するためのルーティング
@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        # 20250227時点ではCRUDの勉強のため論理削除フラグ（delete_flag）は利用しないこととする
        # post.delete_flag = 1
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    elif request.method == 'GET':
        return render_template('delete.html', post=post)

# 投稿の詳細画面を表示するためのルーティング
@app.route('/<int:id>/<string:title>', methods=['GET'])
def post_detail(id, title):
    post = Post.query.get(id)
    return render_template('post_detail.html', post=post)
