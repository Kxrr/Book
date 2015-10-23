#-*- coding: utf-8 -*-

from flask import redirect, flash
from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user, login_required
from app.models import User, BookInfo
from . import admin


class UserView(ModelView):
    column_searchable_list = ['username', 'email', 'nickname']
    column_exclude_list = ['password']
    column_labels = dict(owned_book=u'贡献的书', borrowed_book=u'在借的书',
                         wanted_book=u'收藏的书')

    @login_required
    def is_accessible(self):
        if current_user.role == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash(u'权限不足')
        return redirect('/')


class BookView(ModelView):

    def is_accessible(self):
        if current_user.role == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash(u'权限不足')
        return redirect('/')
    column_exclude_list = ['detail', 'tags', 'img_url', 'online_url', 'rate', 'author']


admin.add_view(UserView(User, name=u'用户'))
admin.add_view(BookView(BookInfo, name=u'书籍'))