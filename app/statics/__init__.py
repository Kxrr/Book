#-*- coding: utf-8 -*-                                                                                     

from flask import Blueprint

statics = Blueprint('statics', __name__)

from . import views