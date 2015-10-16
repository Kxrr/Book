#-*- coding: utf-8 -*-                                                                                     

from flask import Blueprint

backgroud = Blueprint('background', __name__)

from . import views

