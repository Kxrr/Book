# -*- coding: utf-8 -*-
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'key'
SESSION_TYPE = 'mongodb'
WTF_CSRF_ENABLED = False

MAIL_SERVER = 'smtp.sina.com'
MAIL_USERNAME = 'user'
MAIL_PASSWORD = 'password'
MAIL_SUB_PREFIX = 'BookRoom '

MONGO_DATABASE = dict(host='mongodb://localhost:27017/BookRoom')

PAGE_LIMIT = 100
