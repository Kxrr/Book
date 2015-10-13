#-*- coding: utf-8 -*

from app import app
from flask import render_template, request, redirect, url_for
from models import SpiderForm, BookInfo

from untils.spiders import DoubanSpider, JdSpider

@app.route('/')
def index():
    books = BookInfo.objects
    return render_template('index.html', books=books)


@app.route('/manager')
def manager():
    form = SpiderForm()
    books = BookInfo.objects
    return render_template('manager.html', form=form, books=books)

@app.route('/add_from_url', methods=['POST'])
def add_from_url():
    form = SpiderForm(request.form)
    raw_url = form.raw_url.data
    if 'douban' in raw_url:
        spider_book = DoubanSpider(raw_url)
        spider_book.start()
        spider_book.scrub_content()
        return 'Done.'
    elif 'jd' in raw_url:
        JdSpider(raw_url).start()
        return 'Working'
    else:
        return 'Wrong!'
