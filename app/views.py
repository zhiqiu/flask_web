# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename

from app import app, db, lm, oid, scheduler, open_excel, myjob
from flask import render_template
from .forms import *
from .db_models import User, Post, DailyFile, ROLE_USER, ROLE_ADMIN
import MySQLdb
import time
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import math, os, re, json
from werkzeug.security import  generate_password_hash,check_password_hash
from flask import Flask,render_template,request,url_for, make_response,redirect,  send_from_directory

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xls', 'xlsx'])






def getPosts(user):
    posts= db.session.query(Post).filter_by(user_id=user.id).all()
    p = []
    for post in posts:
        postname = post.postname[:post.postname.rindex('_')] + post.postname[post.postname.rindex('.'):]
        timestamp =  post.timestamp
        p += [{'username':user.username,"postname": postname,"timestamp":timestamp, 'uri_name':post.postname}] 
    return p

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/date')
def date():
    return render_template('date.html')
 

@app.route('/') 
@app.route('/index') 
@login_required
def index():

    user = g.user # fake user
#    return user.getPosts()[0]
    return render_template("index.html",
        title = 'Home', user= user, posts = getPosts(user))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
     
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['remember_me'] = form.remember_me.data
        user = db.session.query(User).filter_by(username=username).first()
        #user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
#        session['logged_in'] = True
            flash("登录成功！")
            return redirect(url_for('index'))
        else:
            flash("账号或密码错误，请重新输入")
    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    #session.pop('logged_in', None)
    #flash('You were logged out')
   # return redirect(url_for('index'))

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        new_user=User(username=username, password=generate_password_hash(password),email = email, phone=phone, role=ROLE_USER)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@lm.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    # posts= db.session.query(Post).filter_by(user_id=user.id).all()

#@app.after_request
#def after_request(response):
#     pass
#    db.session.close()
    

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.query(User).filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    return render_template('user.html',
                           user=user,
                           posts=getPosts(user))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    user = g.user
    if request.method == 'GET':
        return render_template("upload.html", title = '上传文件', user = user, posts= getPosts(user))
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            timestamp = datetime.datetime.now()
            showtime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
	    #filename = secure_filename(file.filename)
            filename = file.filename
            filename = filename[:filename.rindex('.')] + '_' + str(timestamp) + filename[filename.rindex('.'):]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("文件%s上传成功，时间%s"%(file.filename,showtime))
        #db_insert
            new_post=Post(filename,timestamp=timestamp,user_id =  user.id)
            db.session.add(new_post)
            db.session.commit()
#        db.session.close()
            return redirect(url_for('upload'))
        else:
            return 'file type not allowed!'
    return render_template('upload.html',)

@app.route('/uploads/<postname>')
@login_required
def uploads(postname):
    return send_from_directory(app.config['UPLOAD_FOLDER'], postname)

@app.route('/all_posts', methods=['GET','POST'])
@login_required
def all_posts():
    user = g.user
    if request.method == 'GET':
        if user.role == ROLE_ADMIN:
            posts= db.session.query(Post).all()
            p = []
            #return str(len(posts))
            for post in posts:
                postname = post.postname[:post.postname.rindex('_')] + post.postname[post.postname.rindex('.'):]
                timestamp =  post.timestamp
                username = db.session.query(User).filter(User.id==post.user_id).first().username
                p += [{'username':username,"postname": postname,"timestamp":timestamp, 'uri_name':post.postname}] 
            return render_template('all_posts.html',user = user, posts = p)
        else:
            return '你没有权限访问这个页面'
    if request.method == 'POST': 
        postname = request.files['postname']
        

@app.route('/daily', methods = ['GET', 'POST'])
@login_required
def daily():
    user = g.user
    if request.method == 'GET':
            #dailyfile= db.session.query(DailyFile).all()
            #dailys = []
            #return str(len(posts))
            #for d in dailyfile:
            #    dailys += [{'filename':d.filename}] 
        return render_template('daily.html')
    if request.method == 'POST': 
        if user.role == ROLE_ADMIN:
            customer_name = request.form['customer_name']             
            begin_date = request.form['begin_date']             
            end_date = request.form['end_date']
            username = customer_name
            user = db.session.query(User).filter_by(username=customer_name).first()
            if user is not None or username == u'所有客户':
                begindate = datetime.datetime.strptime(begin_date,'%m/%d/%Y')
                enddate = datetime.datetime.strptime(end_date,'%m/%d/%Y')
                myjob(username, begindate, enddate)
                filename = username + '_' + begindate.strftime("%Y-%m-%d") + '_' + enddate.strftime("%Y-%m-%d") + '.xls'
                return send_from_directory(app.config['DAILY_FOLDER'], filename)
            else:
                flash("无此客户")
                return render_template('daily.html')
        else:
            customer_name = g.user.username             
            begin_date = request.form['begin_date']             
            end_date = request.form['end_date']
            username = customer_name
            user = db.session.query(User).filter_by(username=customer_name).first()
            if user is not None :
                begindate = datetime.datetime.strptime(begin_date,'%m/%d/%Y')
                enddate = datetime.datetime.strptime(end_date,'%m/%d/%Y')
                myjob(username, begindate, enddate)
                filename = username + '_' + begindate.strftime("%Y-%m-%d") + '_' + enddate.strftime("%Y-%m-%d") + '.xls'
                return send_from_directory(app.config['DAILY_FOLDER'], filename)
            else:
                flash("无该项数据")
                return render_template('daily.html')

      
@app.route('/dailys/<filename>')
@login_required
def dailys(filename):
    user = g.user
    if user.role == ROLE_ADMIN:
        return send_from_directory(app.config['DAILY_FOLDER'], filename)
    else:
        return '你没有权限访问这个页面'



#@app.before_first_request
#def initialize():
    #scheduler.start()
    #scheduler.add_job(myjob, 'interval', seconds = 15, start_date=('2016-01-18 12:19:00'))
    #scheduler.start()


