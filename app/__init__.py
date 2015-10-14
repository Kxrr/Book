#-*- coding: utf-8 -*-

from flask import Flask, url_for
from flask import Blueprint
from config import Config

def creat_app():
    app = Flask(__name__)
    # app.config.from_object(Config[config_name])
    # Config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

