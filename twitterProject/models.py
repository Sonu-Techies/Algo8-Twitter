from datetime import datetime

from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as serializer
from . import db, create_app


class UserManagement(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(500),nullable=False)

    def get_token(self, expire_sec=300):
        """
        
        """
        serial = serializer(create_app.config['SECRET_KEY'], expires_in=expire_sec)
        return serial.dump({"user_id": self.id})

    @staticmethod
    def verified_token(token):
        serial = serializer(create_app.config['SECRET_KEY'])
        try:
            user_id = serial.load(token)['user_id']
        except:
            return None

        return UserManagement.query.get(user_id)
    
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet = db.Column(db.String(500),nullable=False)
    stamp = db.Column(db.String(20),nullable=False)
    post_img = db.Column(db.String(20))
    user_id=db.Column(db.Integer, db.ForeignKey(UserManagement.id), nullable=False)

class Retweet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer,db.ForeignKey(UserManagement.id),nullable=False)
    retweet_stamp = db.Column(db.String(20),nullable=False)
    retweet_text = db.Column(db.String(500),nullable=False)

    timeline = db.relationship('Timeline',backref='from_retweet',lazy=True)

class Timeline(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),default=None)
    retweet_id = db.Column(db.Integer,db.ForeignKey('retweet.id'),default=None)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('usermanagement.id'),default=None)