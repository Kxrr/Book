#-*- coding: utf-8 -*

from mongoengine import DynamicDocument, connect, StringField, ListField, FloatField, DateTimeField
from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

connect('BookRoom')

class BookInfo(DynamicDocument):
    title = StringField(primary_key=True)
    author = StringField()
    rate = FloatField()
    detail = ListField(StringField())
    tags = ListField(StringField())
    category = StringField()
    raw_url = StringField()
    update_time =DateTimeField(default=datetime.now())

    meta = {'collection': 'BookInfo', 'ordering': ['-update_time']}


class User(DynamicDocument):
    username = StringField()
    password = StringField()
    real_name = StringField()


class Delivery(DynamicDocument):
    pass



SpiderForm = model_form(BookInfo)
