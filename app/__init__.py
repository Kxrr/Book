# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)

mailbox = Mail()
mailbox.init_app(app)

from .main import main as main_blueprint
from .login import login as login_blueprint
from .profile import profile as profile_blueprint
from .detail import detail as detail_blueprint
from .manager import manager as manager_blueprint
from .ranking import ranking as ranking_blueprint

app.register_blueprint(login_blueprint)  # login: 用户登录, 用户注册, 验证系统
app.register_blueprint(profile_blueprint)  # profile: 用户自己的信息, 借了哪些书, 记录
app.register_blueprint(main_blueprint)  # main: 展示在架书籍
app.register_blueprint(detail_blueprint)  # detail: 书籍详情页
app.register_blueprint(manager_blueprint)  # manager: 管理图书,添加图书
app.register_blueprint(ranking_blueprint)  # ranking: 排行榜

from app import admin

