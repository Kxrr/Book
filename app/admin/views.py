#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, url_for, flash
from app.models import BookInfo, User, Operation
from app.models import SpiderForm, UserForm
from app.utils.spiders import DoubanSpider
from flask.ext.login import login_required, current_user

from . import admin

@admin.route('/Manager')
def manager():
    if current_user.is_active():  # TODO: 管理role
        books = BookInfo.objects
        return render_template('manager.html', books=books, user=current_user)

@admin.route('/add_from_url', methods=['POST'])
def add_from_url():
    raw_url = request.form['raw_url']
    owner = request.form['owner']
    if not owner:
        owner = current_user.real_name
    if 'book.douban' in raw_url:
        spider_book = DoubanSpider(url=raw_url, owner=owner)
        spider_book.start()
        spider_book.scrub_content()
        flash(u'添加成功')
        Operation(type='add', url_info=raw_url,
                  user=User.objects(id=current_user.id).first()).save()
        return redirect('/Manager')
    elif 'jd' in raw_url:
        return 'Under Working'
    else:
        flash(u'暂不支持该链接')
        return redirect('/Manager')