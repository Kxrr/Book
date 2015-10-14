#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, url_for
from models import BookInfo, User
from models import SpiderForm, UserForm

from . import user

@user.route('/Register')
def register():
    register_form = UserForm()
    return render_template('register.html', form=register_form)

@user.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = UserForm(request.form)
    if register_form_info.validate():
        User(username=register_form_info.username.data, password=register_form_info.password.data,
             real_name=register_form_info.real_name.data).save()
        return 'Register done.'
    else:
        return 'Wrong!'

#

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

        # ...