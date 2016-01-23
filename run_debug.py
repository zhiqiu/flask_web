#!flask/bin/python 
# -*- coding:utf-8 -*-  

from app import app, myjob


if __name__ == '__main__':
    app.run( host = '115.28.41.44', port = 8080, debug = False)
