#-*- coding: utf-8 -*-

from app import mailbox
from app import app
from flask_mail import Message
from flask import render_template
from threading import Thread


def send_async_email(msg):
    with app.app_context():
        mailbox.send(msg)
        return True


def send_email(rec, html_content, subject, subject_prefix='[聘宝藏经阁] '):
    if not isinstance(rec, list):
        rec = [rec]
    msg = Message(subject_prefix + subject, sender="random009s@sina.com", recipients=rec)
    msg.html = html_content
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()
    return True


def send_fav_noti_to_owner(user, user_to, book):
    html_content = render_template('mail/fav_to_owner.html', user=user, user_to=user_to, book=book)
    send_email(rec=user_to.email, html_content=html_content, subject='有人收藏了你的书～')


def send_fav_noti_to_borrowed(user, user_to, book):
    html_content = render_template('mail/fav_to_borrowed.html', user=user, user_to=user_to, book=book)
    send_email(rec=user_to.email, html_content=html_content, subject='有人收藏了你正在看的书～')


def send_borrow_noti_to_owner(user, user_to, book):
    html_content = render_template('mail/borrow_to_owner.html', user=user, user_to=user_to, book=book)
    send_email(rec=user_to.email, html_content=html_content, subject='有人希望借阅你的书～')