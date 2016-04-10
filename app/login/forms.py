#-*- coding: utf-8 -*-

"""
Flask Wtf : http://docs.pythontab.com/flask/flask0.10/patterns/wtforms.html
"""
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Required, Length


class RegisterForm(Form):
    username = StringField(u'用户名', [Length(min=2, max=25)])
    email = StringField(u'邮箱', [Length(min=6, max=32)])
    password = PasswordField(u'密码', [
        Length(min=6, max=32),
        Required(),
    ])


class LoginForm(Form):
    username = StringField(u'用户名', [validators.Length(min=2, max=25)])
    password = PasswordField(u'密码', [validators.Required()])