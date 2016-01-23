# -*- coding:utf-8 -*-  
#!flask/bin/python 

from flask import Flask
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
import os
import sys
sys.path.append("..")
from  shaoguan.config import SQLALCHEMY_DATABASE_URI
#basedir = os.path.abspath(os.path.dirname(__file__))
#from ../config import basedir  
#print basedir
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1340830@localhost/flask'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(128), unique = False)
    email = db.Column(db.String(120), unique = True)
    phone = db.Column(db.String(20), unique = False)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    def __init__(self, username, password, email, phone, role=ROLE_USER):
	self.username = username
	self.email = email
	self.password = password
	self.phone=phone
	self.role = role
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
    postname = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def getName(id):
	post = db.session.query(Post).filter_by(id=id).first()
	if post is not None:
	    return post.postname

    def __repr__(self):
        return '<Post %r>' % (self.body)


    def __init__(self, postname, timestamp, user_id):
	self.postname = postname
	self.timestamp = timestamp
	self.user_id = user_id

class DailyFile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(140))
    date = db.Column(db.DateTime)
    
    def getName(id):
	file = db.session.query(DailyFile).filter_by(id=id).first()
	if file is not None:
	    return file.postname

    def __repr__(self):
        return '<DailyFile %r>' % (self.body)


    def __init__(self, filename, date):
	self.filename = filename
	self.date = date

if __name__ == '__main__':
        db.create_all()



