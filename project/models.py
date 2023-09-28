from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloglite.db'
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()

class Followers(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    follower = db.relationship('User', foreign_keys=[follower_id], backref='followers')
    following = db.relationship('User', foreign_keys=[following_id], backref='following')

class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    bio = db.Column(db.String(100), nullable=False,default='default')
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    picture = db.Column(db.BLOB, nullable=False)
    up_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
        
  
        
    