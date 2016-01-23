#!flask/bin/python 
# -*- coding:utf-8 -*-  

from app import app, myjob


if __name__ == '__main__':
    app.run( host = '0.0.0.0', port = 5000, debug = True)
