from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

from werkzeug.security import  generate_password_hash,check_password_hash
from flask import Flask,render_template,request,url_for, make_response,redirect,  send_from_directory


class LoginForm(Form):
	username = StringField('username',validators = [DataRequired()])
	password = PasswordField('password', validators = [DataRequired()])
	remember_me = BooleanField('remember_me', default = False)


class RegisterForm(Form):
	username = StringField('username',validators = [DataRequired()])
	password = PasswordField('password', validators = [DataRequired()])
	remember_me = BooleanField('remember_me', default = False)
