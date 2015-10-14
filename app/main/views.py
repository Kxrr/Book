#-*- coding: utf-8 -*


from flask import render_template, request, redirect, url_for
from models import BookInfo, User
from models import SpiderForm, UserForm

from untils.spiders import DoubanSpider
from . import main

@main.route('/')
def index():
    books = BookInfo.objects
    return render_template('index.html', books=books)

@main.route('/borrow_book/<string:book_id>')
def borrow_book(book_id):
    return book_id

#


#


        
