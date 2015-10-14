#-*- coding: utf-8 -*


from flask import render_template, request, redirect, url_for
from models import BookInfo, User
from models import SpiderForm, UserForm

from untils.spiders import DoubanSpider

@app.route('/')
def index():
    books = BookInfo.objects
    return render_template('index.html', books=books)

@app.route('/borrow_book/<string:book_id>')
def borrow_book(book_id):
    return book_id

#

@app.route('/Manager')
def manager():
    spider_form = SpiderForm()
    books = BookInfo.objects
    return render_template('manager.html', form=spider_form, books=books)

@app.route('/add_from_url', methods=['POST'])
def add_from_url():
    spider_form_info = SpiderForm(request.form)
    raw_url = spider_form_info.raw_url.data
    if 'douban' in raw_url:
        spider_book = DoubanSpider(raw_url)
        spider_book.start()
        spider_book.scrub_content()
        return 'Done.'
    elif 'jd' in raw_url:
        return 'Working'
    else:
        return 'Wrong!'

#

@app.route('/Register')
def register():
    register_form = UserForm()
    return render_template('register.html', form=register_form)

@app.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = UserForm(request.form)
    if register_form_info.validate():
        User(username=register_form_info.username.data, password=register_form_info.password.data,
             real_name=register_form_info.real_name.data).save()
        return 'Register done.'
    else:
        return 'Wrong!'

#

@app.route('/Login')
def login():
    login_form = UserForm()
    return render_template('login.html', form=login_form)

@app.route('/handle_login', methods=['POST'])
def handle_login():
    login_form_info = UserForm(request.form)
    if login_form_info.validate():
        username = login_form_info.username.data
        password = login_form_info.password.data

        # ...
        
