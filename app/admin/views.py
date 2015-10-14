#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, url_for, flash
from app.models import BookInfo, User
from app.models import SpiderForm, UserForm
from app.untils.spiders import DoubanSpider

from . import admin

@admin.route('/Manager')
def manager():
    spider_form = SpiderForm()
    books = BookInfo.objects
    return render_template('manager.html', form=spider_form, books=books)

@admin.route('/add_from_url', methods=['POST'])
def add_from_url():
    spider_form_info = SpiderForm(request.form)
    raw_url = spider_form_info.raw_url.data
    if 'douban' in raw_url:
        spider_book = DoubanSpider(raw_url)
        spider_book.start()
        spider_book.scrub_content()
        flash(u'添加成功')
        return redirect('/Manager')
    elif 'jd' in raw_url:
        return 'Working'
    else:
        return 'Wrong!'
