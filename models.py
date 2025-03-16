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
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # Flask-Loginでは"id"を定義しないといけないが、"user_id"としてしまったのでget_id()をオーバーライドしている
    def get_id(self):
        return str(self.user_id)