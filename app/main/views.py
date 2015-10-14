#-*- coding: utf-8 -*


from flask import render_template, request, redirect, url_for
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
    return book_id

