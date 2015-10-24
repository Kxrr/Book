#-*- coding: utf-8 -*-

from app import mailbox
from flask_mail import Message


def send_email(rec, content, subject='来自聘宝藏经阁的通知'):
    if not isinstance(rec, list):
        rec = [rec]
    msg = Message(subject, sender="random009s@sina.com", recipients=rec)
    msg.html = content
    return mailbox.send(msg)
