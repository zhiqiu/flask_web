# -*- coding:utf-8 -*-  

from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
import os
import MySQLdb
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir 
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import xlrd, xlwt
from flask_bootstrap import Bootstrap


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__) 
app.config.from_object('config')

db  = SQLAlchemy(app)
Bootstrap(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.session_protection = "strong"
lm.login_message = u'请先登录！'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)
            

 
# 每天凌晨0点合并当天的表格
def myjob(username, begin_date, end_date):
    print username, begin_date, end_date 
    db = MySQLdb.connect(host="localhost",user="root",passwd="1340830",db="flask",charset='utf8' )
    cursor = db.cursor()
    if username == u'所有客户':
        cursor.execute( "select * from post")
    else:
        cursor.execute('select id from user where user.username = %s'% (username))
        user_id = cursor.fetchone()
        cursor.execute('select * from post where post.user_id = %s'% (user_id))
    #cursor.execute(sql)
    #print datetime.now()
    res = cursor.fetchall()
    workbook = xlwt.Workbook()
    out = workbook.add_sheet('Sheet')
    outrow_idx = 0
    firstfile = True
    if len(res) == 0:
        pass
    else:
    
        for row in res:
            postname = row[1]
            timestamp = row[2]
            #yesterday = datetime.today() - timedelta(days=1) 
            if timestamp.date()<= end_date.date() and timestamp.date() >= begin_date.date():
            #if timestamp.hour== yesterday.hour:
                file = app.config['UPLOAD_FOLDER']+postname
                #print file, os.path.exists(file)
                try:
                    data = open_excel(file).sheets()[0]
                    for row_idx in xrange(0 if firstfile else 1, data.nrows):
                        for col_idx in xrange(data.ncols):
                            out.write(outrow_idx, col_idx, data.cell_value(row_idx, col_idx))
                        outrow_idx += 1
                    firstfile = False
                except Exception, e:
                    print e
        
        filename = username + '_' + begin_date.strftime("%Y-%m-%d") + '_' + end_date.strftime("%Y-%m-%d") + '.xls'
        #        return send_from_directory(app.config['DAILY_FOLDER'], filename)
        #filename = yesterday.strftime("%Y-%m-%d")+'.xls'
        outpath = os.path.join(app.config['DAILY_FOLDER'],filename)
        workbook.save(outpath)

        cursor.execute( 'insert into daily_file values(%s,%s,%s )', (0, filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S') ))
    

    db.commit()
    db.close()
    #print len(results)
    print datetime.now()
 

scheduler = BackgroundScheduler()
#scheduler = APScheduler()
#scheduler.init_app(app)
#scheduler.start()

#scheduler.add_job(myjob, 'interval', hours = 24, start_date=('2016-01-22 00:00:00'))
#scheduler.start()
from app import views

