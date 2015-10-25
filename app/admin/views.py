#-*- coding: utf-8 -*-

from flask import redirect, flash
from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user, login_required
from app.models import User, BookInfo
from . import admin


class UserView(ModelView):
    column_searchable_list = ['username', 'email', 'nickname', 'real_name']
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
    column_searchable_list = ['title', 'raw_url',]
    column_choices = {
        'deleted': [
            (True, u'已删除'),
            (False, u'正常'),
        ],
        'category':[
            (u'tech', u'技术'),
            (u'literature', u'文学'),
            (u'art', u'设计'),
            (u'math', u'数理'),
            (u'manager', u'管理'),
            (u'economy', u'经济'),]
    }

    def is_accessible(self):
        if current_user.role == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash(u'权限不足')
        return redirect('/')
    column_exclude_list = ['detail', 'tags', 'img_url', 'online_url', 'rate', 'author']

    def get_query(self):
        # 将被设置为deleted的书也展示出来
        queryset = self.model.get_all()
        return queryset


class BookRoomView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')


admin.add_view(UserView(User, name=u'用户'))
admin.add_view(BookView(BookInfo, name=u'书籍'))
admin.add_view(BookRoomView(name=u'藏经阁'))