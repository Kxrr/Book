#-*- coding: utf-8 -*

from flask import render_template, redirect, flash, request
from app.models import BookInfo, User, Operation
from . import statics
from flask.ext.login import login_user, logout_user, current_user, login_required

"""
数目owner排序,借阅数排序,数目借阅量排序,简单处理为从系统开始运行后sum.
"""

@statics.route('/Statics')
def do_statics():
    # own_most = BookInfo.objects.sort('-owner')
    return render_template('statics.html')
