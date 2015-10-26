#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, flash
from app.models import BookInfo, User, Operation
from app.utils.spiders import DoubanSpider, DoubanReadSpider
from flask.ext.login import login_required, current_user

from . import manager
import re

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
        urls = re.split(u",|，", raw_url)
        for url in urls:
            if url:
                url = url.strip()
                spider = DoubanSpider(url=url, owner_id=owner_id, online_url=online_url)
                spider.crawl()
                parse = spider.parse_content()
                if parse:
                    flash(u'感谢小伙伴: {}, 为聘宝添砖加瓦了, 「{}」, 添加成功 '
                          .format(current_user.nickname, spider.content_dict.get('title')))
                else:
                    flash(u'{}, 添加失败, 请联系管理员'.format(url))
                Operation(type='add', url_info=raw_url,
                          user=User.objects.get(id=current_user.id),
                          success=True if parse else False).save()
        return redirect('/Manager')
    elif 'read.douban' in raw_url:
        flash(u'暂不支持来自豆瓣阅读的图书')
        return redirect('/Manager')
    elif 'jd' in raw_url:
        return 'Under Working'
    else:
        flash(u'暂不支持该链接, 请使用豆瓣图书的链接')
        Operation(type='add', url_info=raw_url,note='not support',
                  user=User.objects.get(id=current_user.id)).save()
        return redirect('/Manager')

@manager.route('/add_by_input', methods=['POST'])
def add_by_input():
    pass