#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, redirect, url_for, flash
from models import BookInfo, User
from . import profile
from flask.ext.login import login_user, logout_user, current_user

@profile.route('/MyInfo')
def profile_info():
    user_obj = User.objects(id=current_user.id).first()
    user_borrowed_objs = user_obj.borrowed_book

    return render_template('profile.html', books=user_borrowed_objs)

@profile.route('/return_book/<string:book_id>')
def return_book(book_id):
    user_obj = User.objects(id=current_user.id).first()
    book_obj = BookInfo.objects(id=book_id).first()

    if book_obj.user_borrowed.id == user_obj.id:
        print type(book_obj)
        user_obj.update(pull__borrowed_book=book_obj)
        book_obj.update(on_bookshelf=True, unset__user_borrowed=1)
        flash(u'Done.')
        return redirect('/')

    return 'wrong!'

