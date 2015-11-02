#-*- coding: utf-8 -*-

from flask_admin import Admin
from .. import app

admin = Admin(app, template_mode='bootstrap3', name='BookRoomAdmin')

from . import views

