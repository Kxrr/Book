#-*- coding: utf-8 -*-

from flask import Flask, url_for
from flask import Blueprint



app = Flask(__name__)
app.config.from_object('config')

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)  # 展示在架书籍

from .user import user as user_blueprint
app.register_blueprint(user_blueprint)  # 用户登录, 验证

# profile 用户信息, 借了哪些书, 记录



from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)  # 管理图书, 用户