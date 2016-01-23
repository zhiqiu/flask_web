# -*- coding:utf-8 -*-  

import os

basedir = os.path.abspath(os.path.dirname(__file__))

## use sqlite 
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True

# this is mysql config
# uri = 'mysql://user:psaaword@host/db_name'
SQLALCHEMY_DATABASE_URI = 'mysql://root:1340830@localhost/flask?charset=utf8'

# this is uploads folder config
UPLOAD_FOLDER = os.path.join(basedir,'app/uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xls'])

# daily file folder
DAILY_FOLDER = os.path.join(basedir,'app/daily/')


# apscheduler jobs

#csrf 跨站请求保护
SECRET_KEY = 'protect/csrf/secret/key!'
