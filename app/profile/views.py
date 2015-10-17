#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, redirect, url_for, flash
from app.models import BookInfo, User, Operation, Delivery
from . import profile
from flask.ext.login import current_user, login_required

from datetime import datetime

@profile.route('/MyInfo')
def profile_info():
    user_obj = User.objects(id=current_user.id).first()
    user_borrowed_books = user_obj.borrowed_book
    deliverys = Delivery.objects(user=user_obj)
    now = datetime.now()
    return render_template('profile.html', books=user_borrowed_books, user=user_obj, deliverys=deliverys, now=now)

@profile.route('/return_book/<string:book_id>')
@login_required
def return_book(book_id):
    user_obj = User.objects(id=current_user.id).first()
    book_obj = BookInfo.objects(id=book_id).first()

    if book_obj.user_borrowed.id == user_obj.id:
        user_obj.update(pull__borrowed_book=book_obj)
        book_obj.update(on_bookshelf=True, unset__user_borrowed=1)
        flash(u'「{}」, 归还成功'.format(book_obj.title))
        Operation(type='return', user=user_obj, book_info=book_obj).save()
        Delivery.objects(user=user_obj, book=book_obj).update(set__return_time=datetime.now(), set__returned=True)
        return redirect('/')
    else:
        flash(u'非法操作')
        return redirect('/')

@profile.route('/Profile/<string:id>')
def user_info(id):
    user = User.objects(id=id).first()
    deliverys = Delivery.objects(user=user)
    return render_template('profile_pub.html', user=user, deliverys=deliverys)

@profile.errorhandler(401)
def un_authorized(e):
    flash(u'此操作需要登录')
    # return redirect(url_for('user.login')), 401
    return redirect('/Login')

