#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, flash
from app.models import BookInfo, User, Operation
from app.utils.spiders import DoubanSpider, DoubanReadSpider, JdSpider
from flask.ext.login import login_required, current_user

from . import backgroud

@backgroud.route('/Manager')
def manager():
    if current_user.is_active():  # TODO: 管理role
        books = BookInfo.objects
        return render_template('manager.html', books=books, user=current_user)

@backgroud.route('/add_from_url', methods=['POST'])
def add_from_url():
    raw_url = request.form['raw_url']
    # owner = User.objects(nickname=request.form['owner']).first()  # TODO: 做选框
    # if not owner:  #
    #     owner = current_user.nickname
    owner = current_user.nickname
    if 'book.douban' in raw_url:
        spider = DoubanSpider(url=raw_url, owner=owner)
        spider.crawl()
        spider.parse_content()
        flash(u'添加成功')
        Operation(type='add', url_info=raw_url,
                  user=User.objects(id=current_user.id).first()).save()
        return redirect('/Manager')
    elif 'read.douban' in raw_url:
        spider = DoubanReadSpider(url=raw_url, owner=owner)
        spider.crawl()
        spider.parse_content()
        Operation(type='add', url_info=raw_url,
                  user=User.objects(id=current_user.id).first()).save()
        return redirect('/Manager')

    elif 'jd' in raw_url:
        return 'Under Working'
    else:
        flash(u'暂不支持该链接')
        return redirect('/Manager')

@backgroud.route('/add_by_input', methods=['POST'])
def add_by_input():
    pass