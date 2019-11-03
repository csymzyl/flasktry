from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://recipeadm:1234@localhost:3306/recipe_recommendation"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

#创建模型对象
class User(UserMixin,db.Model):
    __tablename__='user_basicinfo'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)

    @property
    def password(self):  # 外部使用
        return self._password

    @password.setter
    def password(self, row_password):
        self._password = generate_password_hash(row_password)

    def check_password(self, row_password):
        result = check_password_hash(self._password, row_password)
        return result

class user_character(UserMixin,db.Model):
    __tablename__='user_character'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activity = db.Column(db.String(120), unique=True, nullable=False)
    weight = db.Column(db.Integer, unique=True, nullable=False)
    height = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer, unique=True, nullable=False)
    region = db.Column(db.String(120), unique=True, nullable=False)
    flavour = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)

 #   def __repr__(self):
 #       return '<User %r>' % self.email


db.create_all()
