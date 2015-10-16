#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, url_for, flash
from app.models import BookInfo, User
from app.models import SpiderForm, UserForm
from app import app
from . import user
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(id):
    user = User.objects(id=id)
    if user:
        return user.first()
    else:
        return ''

@user.route('/Register')
def register():
    register_form = UserForm()
    return render_template('register.html', form=register_form)

@user.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = UserForm(request.form)
    if register_form_info.validate():
        if User.objects(username=register_form_info.username.data):
            flash(u'用户名己被注册')
            return redirect('/Register')
        else:
            new_user = User(username=register_form_info.username.data, password=register_form_info.password.data,
                            nickname=register_form_info.nickname.data, email=register_form_info.email.data)
            new_user.save()
            flash(u'注册成功, 自动登录还没做, 自个登吧')
            # TODO: 需要自动登录
            return redirect('/Login')
    else:
        flash(u'信息不对')
        return redirect('/Register')

@user.route('/Login')
def login():
    login_form = UserForm()
    return render_template('login.html', form=login_form)

@user.route('/handle_login', methods=['POST'])
def handle_login():
    login_form_info = UserForm(request.form)
    if login_form_info.validate():
        username = login_form_info.username.data
        password = login_form_info.password.data
        if '@' in username:
            user_online = User.objects(email=username, password=password)
        else:
            user_online = User.objects(username=username, password=password)

        if user_online:
            login_user(user=user_online.first(), remember=True)
            return redirect('/')
        else:
            flash(u'帐号与密码不匹配')
            return redirect('/Login')
    else:
        flash(u'非法输入')
        return redirect('/Login')

@user.route('/handle_logout')
def handle_logout():
    logout_user()
    flash(u'己登出')
    return redirect('/')

@user.route('/test_login')
@login_required
def test_login():
    print current_user.username
    return '~~~~'

