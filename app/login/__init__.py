#-*- coding: utf-8 -*-                                                                                     

from flask import Blueprint

login = Blueprint('login', __name__)

from . import views