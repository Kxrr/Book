#-*- coding: utf-8 -*


from flask import render_template, redirect, url_for, flash
from models import BookInfo, User
from . import main
from flask.ext.login import login_user, logout_user, current_user

@main.route('/')
def index():
    user_online_obj = current_user
    books = BookInfo.objects.filter(on_bookshelf=True)
    return render_template('index.html', books=books, user=user_online_obj)

@main.route('/borrow_book/<string:book_id>')
def borrow_book(book_id):
    print book_id
    book_obj = BookInfo.objects(id=book_id).first()
    print book_obj.title
    print dir(book_obj)
    user_online_obj = User.objects(id=current_user.id).first()  # Watch out, current_user is <class 'werkzeug.local.LocalProxy'>
    print type(user_online_obj)
    book_obj.update(set__on_bookshelf=False, user_borrowed=user_online_obj)
    user_online_obj.update(push__borrowed_book=book_obj)

    # TODO: 设置归还时间,异常处理
    flash(u'{}, 借阅成功'.format(book_obj.title))
    return redirect('/')




