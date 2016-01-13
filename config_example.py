# -*- coding: utf-8 -*-
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'key'
SESSION_TYPE = 'mongodb'
WTF_CSRF_ENABLED = False

ADMIN_MAIL = 'i@example.com'

MAIL_SERVER = 'smtp.sina.com'
MAIL_USERNAME = 'user'
MAIL_PASSWORD = 'password'
MAIL_SUB_PREFIX = 'BookRoom '

MONGO_DATABASE = dict(host='mongodb://user:password@localhost:27017/books')

PAGE_LIMIT = 100
