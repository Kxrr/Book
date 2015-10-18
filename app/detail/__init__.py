#-*- coding: utf-8 -*-

from flask import Blueprint

detail = Blueprint('detail', __name__)

from . import views