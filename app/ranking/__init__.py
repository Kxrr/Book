#-*- coding: utf-8 -*-

from flask import Blueprint

ranking = Blueprint('ranking', __name__)

from . import views