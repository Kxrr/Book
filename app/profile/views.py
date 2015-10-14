#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, redirect, url_for, flash
from models import BookInfo, User
from . import profile
from flask.ext.login import login_user, logout_user, current_user

@profile.route('/MyInfo')
def profile_info():
    user_obj = User.objects(id=current_user.id).first()
    user_borrowed_objs = user_obj.borrowed_book
    return user_borrowed_objs[3].title
