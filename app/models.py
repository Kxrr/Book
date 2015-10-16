#-*- coding: utf-8 -*

from mongoengine import DynamicDocument, connect, StringField, ListField, FloatField, \
    DateTimeField, BooleanField, ReferenceField
from flask.ext.mongoengine.wtf import model_form
from datetime import datetime, timedelta

connect('BookRoom')

class User(DynamicDocument):
    username = StringField(max_length=15, unique=True, required=True, min_length=5)
    password = StringField(required=True)
    real_name = StringField(min_length=2)
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
    owner = StringField(required=True)

    user_borrowed = ReferenceField(User)

    meta = {'ordering': ['-update_time']}

    def __repr__(self):
        return self.raw_url

class Operation(DynamicDocument):
    """
    @summary: 记录每一次操作
    """
    type = StringField()
    user = ReferenceField(User)
    time = DateTimeField(default=datetime.now())
    book_info = ReferenceField(BookInfo)

    url_info = StringField()

class Delivery(DynamicDocument):
    """
    @summary: 书籍记录和归还时间
    """
    borrow_time = DateTimeField(default=datetime.now())
    deadline = DateTimeField(default=datetime.now() + timedelta(days=30))  # 设置一个月后归还

    user = ReferenceField(User)
    book = ReferenceField(BookInfo)

    return_time = DateTimeField()
    returned = BooleanField(default=False)


SpiderForm = model_form(BookInfo)
UserForm = model_form(User)

# import ipdb; ipdb.set_trace()
# print ''
