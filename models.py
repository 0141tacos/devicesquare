from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(400))
    # imageには保存している画像ファイルのパスを格納する
    image = db.Column(db.String(400))
    # 投稿を作成したユーザーのID
    # 編集・削除ボタンを表示するときの場合分けに利用
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # Flask-Loginでは"id"を定義しないといけないが、"user_id"としてしまったのでget_id()をオーバーライドしている
    def get_id(self):
        return str(self.user_id)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    favorite_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class Follow(db.Model):
    __tablename__ = 'follow'
    # フォローする側
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    # フォローされる側
    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    # フォローした日
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # フォローが重複しないためのユニーク制約
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)