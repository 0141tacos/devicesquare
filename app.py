from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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