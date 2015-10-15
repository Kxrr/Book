#-*- coding: utf-8 -*

from mongoengine import DynamicDocument, connect, StringField, ListField, FloatField, \
    DateTimeField, BooleanField, ReferenceField
from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

connect('BookRoom')

class User(DynamicDocument):
    username = StringField(max_length=10, unique=True, required=True)
    password = StringField(required=True)
    real_name = StringField()
    borrowed_book = ListField(ReferenceField('BookInfo'))
    role = StringField(default='staff')

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)  # Watch out here, needs str
    def __repr__(self):
        return self.username

    meta = {'ordering': ['+username']}

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

    meta = {'ordering': ['-update_time']}

    def __repr__(self):
        return self.raw_url

class Deliver(DynamicDocument):
    start_time = DateTimeField()
    deadline_time = DateTimeField()
    username = ReferenceField(User)


SpiderForm = model_form(BookInfo)
UserForm = model_form(User)

