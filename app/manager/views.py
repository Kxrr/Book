# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash
from ..models import BookInfo, User, Operation
from ..utils.spiders import DoubanSpider, JingDongSpider
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
    urls = re.split(u",|，", raw_url)
    for url in urls:
        url = url.strip()
        parse = None
        print url
        if 'book.douban' in url:
            spider = DoubanSpider(url=url, owner_id=owner_id, online_url=online_url)
            spider.crawl()
            parse = spider.parse_content()
        elif 'jd.com' in url:
            spider = JingDongSpider(url=url, owner_id=owner_id, online_url=online_url)
            spider.crawl()
            parse = spider.parse_content()
        else:
            pass
        if parse:
            flash(u'感谢小伙伴: {}, 为聘宝添砖加瓦了, 「{}」, 添加成功 '
                  .format(current_user.nickname, spider.content_dict.get('title')))
        else:
            flash(u'{}, 添加失败, 请联系管理员'.format(url))
        Operation(type='add', url_info=raw_url,
                  user=User.objects.get(id=current_user.id),
                  success=True if parse else False).save()
    return redirect('/Manager')


@manager.route('/add_by_input', methods=['POST'])
def add_by_input():
    pass
