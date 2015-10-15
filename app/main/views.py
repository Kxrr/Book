#-*- coding: utf-8 -*


from flask import render_template, redirect, flash, request
from app.models import BookInfo, User
from . import main
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.utils.search_mongo import search

@main.route('/')
def index():
    books = BookInfo.objects.filter(on_bookshelf=True)
    return render_template('index.html', books=books, user=current_user)


@main.route('/borrow_book/<string:book_id>')
def borrow_book(book_id):
    if current_user.is_active:
        book_obj = BookInfo.objects(id=book_id).first()
        user_online_obj = User.objects(id=current_user.id).first()  # Watch out, current_user is <class 'werkzeug.local.LocalProxy'>
        print type(user_online_obj)
        book_obj.update(set__on_bookshelf=False, user_borrowed=user_online_obj)
        user_online_obj.update(push__borrowed_book=book_obj)

        # TODO: 设置归还时间,异常处理
        flash(u'「{}」, 借阅成功'.format(book_obj.title))
    else:
        flash(u'失败, 请登录后再操作')
    return redirect('/')


@main.route('/Detail/<string:book_id>')
def book_detail(book_id):
    book_obj = BookInfo.objects(id=book_id).first()
    return render_template('detail.html', book=book_obj)


@main.route('/Search', methods=['POST'])
def handle_search():
    keyword = request.form['keyword'].strip()
    results = search(keyword)
    return render_template('search_result.html', results=results, keyword=keyword, user=current_user)





