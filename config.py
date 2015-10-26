# -*- coding: utf-8 -*-
import os
import platform

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'kxrr'
SESSION_TYPE = 'mongodb'
WTF_CSRF_ENABLED = False  # 会引起登录问题

MAIL_SERVER = 'smtp.sina.com'
MAIL_USERNAME = 'random009s'
MAIL_PASSWORD = 'randomemail'
MAIL_SUB_PREFIX = '[聘宝藏经阁] '

MONGODBDATEBASE = {
    'db': 'BookRoom',
    'host': 'localhost',
    'port': 27017,
}

FLASK_DEBUG = False if platform.uname()[2] == '2.6.32-042stab104.1' else True
FLASK_PORT = 5321

PAGE_LIMIT = 100
