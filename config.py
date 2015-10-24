#-*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

MONGODB_SETTINGS = {'DB':'BookRoom'}
SECRET_KEY = 'kxrr'
WTF_CSRF_ENABLED = False
SESSION_TYPE = 'mongodb'

MAIL_SERVER = 'smtp.sina.com'
MAIL_USERNAME = 'random009s'
MAIL_PASSWORD = 'randomemail'
