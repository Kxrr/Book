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
from .backgroud import backgroud as background_blueprint
from .statics import statics as statics_blueprint

app.register_blueprint(user_blueprint)  # user: 用户登录, 验证系统
app.register_blueprint(profile_blueprint)  # profile: 用户自己的信息, 借了哪些书, 记录
app.register_blueprint(main_blueprint)  # main: 展示在架书籍
app.register_blueprint(background_blueprint)  # manager: 管理图书,添加图书
app.register_blueprint(statics_blueprint)  # statics: 统计借阅数,按owner分



from flask import session

