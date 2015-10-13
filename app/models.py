#-*- coding: utf-8 -*

from mongoengine import DynamicDocument, connect, StringField, ListField, FloatField, \
    DateTimeField, BooleanField, ReferenceField
from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

connect('BookRoom')

class User(DynamicDocument):
    username = StringField(max_length=10, unique=True)
    password = StringField()
    real_name = StringField()

    book_borrowed = ListField(StringField())
    history = ListField(StringField())

class BookInfo(DynamicDocument):
    title = StringField(unique=True)
    author = StringField()
    rate = FloatField()
    detail = ListField(StringField())
    tags = ListField(StringField())
    category = StringField()
    raw_url = StringField()
    update_time = DateTimeField(default=datetime.now())

    on_bookshelf = BooleanField(default=True)
    user_borrowed = ReferenceField(User)

    meta = {'collection': 'BookInfo', 'ordering': ['-update_time']}

class DetailPage(DynamicDocument):
    title = ReferenceField(BookInfo)
    comments = ''

SpiderForm = model_form(BookInfo)
UserForm = model_form(User)