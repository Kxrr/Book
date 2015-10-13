#-*- coding: utf-8 -*-

from flask import Flask, url_for


app = Flask(__name__)
app.config.from_object('config')
app.debug = True


from app import views, models
