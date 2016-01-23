# -*- coding:utf-8 -*-  

from app import db
ROLE_USER = 0
ROLE_ADMIN = 1
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    def __init__(self, nickname, email):
	self.nickname = nickname
	self.email = email
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
 
    def get_id(self):
 	try:
	    return unicode(self.id) 
	except NameError:
	    return str(self.id)
    def check_password(self,password):
	return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User %r>' % (self.username)
 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uri = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return '<Post %r>' % (self.body)
