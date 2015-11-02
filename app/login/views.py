# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash
from flask.ext.login import login_user, logout_user
from flask.helpers import url_for

from ..models import User
from ..login.forms import RegisterForm, LoginForm
from .. import lm
from . import login


@lm.user_loader
def load_user(id):
    return User.objects.get(id=id)


@login.route('/Register')
def register():
    register_form = RegisterForm()
    return render_template('register.html', form=register_form)


@login.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = RegisterForm(request.form)
    if register_form_info.validate():
        if User.objects(username=register_form_info.username.data):
            flash(u'用户名己被注册')
            return register()
        else:
            new_user = User(username=register_form_info.username.data, password=register_form_info.password.data,
                            nickname=register_form_info.nickname.data, email=register_form_info.email.data)
            new_user.save()
            login_user(user=new_user, remember=True)
            flash(u'注册成功, 登录成功')
            return redirect('/')
    else:
        flash(u'用户名或密码不符合要求')
        return register()


@login.route('/Login')
def login_index():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@login.route('/handle_login', methods=['POST'])
def handle_login():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        if '@' in username:
            user = User.objects(email=username)
        else:
            user = User.objects(username=username)
        if user and user.first().verify_password(password):
            login_user(user=user.first(), remember=True)
            return redirect(url_for('main.index'))
        else:
            flash(u'帐号与密码不匹配')
            return login_index()
    else:
        flash(u'非法输入')
        return login_index()


@login.route('/Logout')
def handle_logout():
    logout_user()
    flash(u'己登出')
    return redirect('/')
