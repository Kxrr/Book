#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, flash
from app.models import BookInfo, User, Operation
from app.utils.spiders import DoubanSpider, DoubanReadSpider, JdSpider
from flask.ext.login import login_required, current_user

from . import manager

@manager.route('/Manager')
@login_required
def manager_index():
    if current_user.is_active():  # TODO: 管理role
        books = BookInfo.objects
        users = User.objects(id__ne=current_user.id)
        return render_template('manager.html', books=books, current_user=current_user, users=users)

@manager.route('/add_from_url', methods=['POST'])
def add_from_url():
    raw_url = request.form['raw_url']
    online_url = request.form['online_url']
    owner_id = request.form['owner']
    if 'book.douban' in raw_url:
        spider = DoubanSpider(url=raw_url, owner_id=owner_id, online_url=online_url)
        spider.crawl()
        parse = spider.parse_content()
        if parse:
            flash(u'添加成功')
        Operation(type='add', url_info=raw_url,
                  user=User.objects.get(id=current_user.id)).save()
        return redirect('/Manager')
    elif 'read.douban' in raw_url:
        spider = DoubanReadSpider(url=raw_url, owner_id=owner_id, online_url=online_url)
        spider.crawl()
        parse = spider.parse_content()
        if parse:
            flash(u'添加成功')
        Operation(type='add', url_info=raw_url,
                  user=User.objects.get(id=current_user.id)).save()
        return redirect('/Manager')

    elif 'jd' in raw_url:
        return 'Under Working'
    else:
        flash(u'暂不支持该链接')
        Operation(type='add', url_info=raw_url,note='not support',
                  user=User.objects.get(id=current_user.id)).save()
        return redirect('/Manager')

@manager.route('/add_by_input', methods=['POST'])
def add_by_input():
    pass