#-*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MONGODB_SETTINGS = {'DB':'BookRoom'}
    SCRET_KEY = 'kxrr'
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    pass




