#-*- coding: utf-8 -*-

from flask import Flask, url_for
from flask import Blueprint


app = Flask(__name__)
app.config.from_object('config')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'kxrr'

from .main import main as main_blueprint
from .user import user as user_blueprint
from .profile import profile as profile_blueprint
from .admin import admin as admin_blueprint

app.register_blueprint(user_blueprint)  # 用户登录, 验证
app.register_blueprint(profile_blueprint)  # profile 用户自己的信息, 借了哪些书, 记录
app.register_blueprint(main_blueprint)  # 展示在架书籍
app.register_blueprint(admin_blueprint)  # 管理图书, 用户



from flask import session

