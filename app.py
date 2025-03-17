from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
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
        from api import create_post
        create_post(request)
        return redirect('/')
    else:
        return render_template('create.html')

# 投稿更新画面表示のためのルーティング
@app.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        from api import update_post
        update_post(post, request)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('update.html', post=post)

# 投稿を削除するためのルーティング
@app.route('/<int:post_id>/delete', methods=['GET', 'POST'])
def delete(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        # 20250227時点ではCRUDの勉強のため論理削除フラグ（delete_flag）は利用しないこととする
        # post.delete_flag = 1
        from api import delete_post
        delete_post(post, request)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('delete.html', post=post)

# 投稿の詳細画面を表示するためのルーティング
@app.route('/<int:post_id>/<string:title>', methods=['GET'])
def post_detail(post_id, title):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)
