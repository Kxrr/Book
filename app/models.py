# -*- coding: utf-8 -*
from flask.ext.login import UserMixin
from mongoengine import DynamicDocument, EmbeddedDocument, StringField, ListField, FloatField, \
                        DateTimeField, BooleanField, ReferenceField, EmbeddedDocumentField, IntField
from mongoengine import queryset_manager, connect
from werkzeug.security import generate_password_hash, check_password_hash

from config import MONGO_DATABASE
from datetime import datetime, timedelta

connect('books', **MONGO_DATABASE)

CATEGORY_CHOICES = (
    (u'tech', u'技术'),
    (u'literature', u'文学'),
    (u'art', u'设计'),
    (u'math', u'数理'),
    (u'manager', u'管理'),
    (u'economy', u'经济'),
)

ROLE_CHOICES = (
    (u'staff', u'用户'),
    (u'admin', u'管理员'),
)


class User(DynamicDocument, UserMixin):
    """
    @summary: 用户
    """
    username = StringField(max_length=20, unique=True, required=True, min_length=4)
    email = StringField(unique=True)
    password_hash = StringField()
    nickname = StringField(min_length=1)
    real_name = StringField()
    borrowed_book = ListField(ReferenceField('BookInfo'))
    role = StringField(choices=ROLE_CHOICES, default='staff')
    owned_book = ListField(ReferenceField('BookInfo'))
    wanted_book = ListField(ReferenceField('BookInfo'))  # 没有书时的收藏功能
    confirmed = BooleanField(default=False)

    def get_id(self):
        return str(self.id)  # Watch out here, needs str

    @property
    def str_id(self):
        return str(self.id)

    @property
    def password(self):
        return AttributeError('password is not readable')

    @password.setter
    def password(self, value):
        # TODO: ?
        if not self.password_hash:
            self.password_hash = generate_password_hash(value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self, *args, **kwargs):
        if not self.real_name:
            self.real_name = self.nickname
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.username

    meta = {'ordering': ['+nickname'], 'index_background': False, 'indexes': ['nickname']}


class Comment(EmbeddedDocument):
    """
    @summary: 用户评论
    """
    content = StringField()
    name = ReferenceField(User)
    time = DateTimeField(default=datetime.now)
    meta = {'ordering': ['-id'], 'index_background': True}


class BookInfo(DynamicDocument):
    """
    @summary: 书的信息
    """
    title = StringField(unique=True)
    author = StringField()
    rate = FloatField()
    detail = ListField(StringField())
    tags = ListField(StringField())
    category = StringField(choices=CATEGORY_CHOICES)
    raw_url = StringField()
    online_url = StringField()
    img_url = StringField()
    update_time = DateTimeField(default=datetime.now)
    # on_bookshelf = BooleanField(default=True)
    deleted = BooleanField(default=False)  # 方便实现删除图书操作
    num = IntField(default=1)  # 书籍数量, 对应多本相同书属于不同的人的情况
    owner = ListField(ReferenceField(User))
    user_borrowed = ListField(ReferenceField(User))  # 哪些人正在借
    comment = ListField(EmbeddedDocumentField(Comment))

    meta = {'ordering': ['-id'], 'index_background': False,
            'indexes': ['title', 'tags', 'author', ('-deleted', '-id')]}

    @property
    def str_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.title

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.filter(deleted__ne=True)

    @queryset_manager
    def get_all(doc_cls, queryset):
        return queryset.order_by('-deleted', '-id')


class Operation(DynamicDocument):
    """
    @summary: 记录每一次操作, 不调用
    """
    type = StringField()
    user = ReferenceField(User)
    time = DateTimeField(default=datetime.now)
    book_info = ReferenceField(BookInfo)
    note = StringField()

    url_info = StringField()
    meta = {'ordering': ['-id'], 'index_background': True}


class Delivery(DynamicDocument):
    """
    @summary: 书籍记录和归还时间, 采用单条文档的方式
    """
    borrow_time = DateTimeField(default=datetime.now)
    deadline = DateTimeField()

    user = ReferenceField(User)
    book = ReferenceField(BookInfo)

    return_time = DateTimeField()
    returned = BooleanField(default=False)

    @property
    def str_id(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.deadline:
            self.deadline = self.borrow_time + timedelta(days=30)   # 设置一个月后归还
        super(Delivery, self).save(*args, **kwargs)

    meta = {'ordering': ['-id'], 'index_background': True, 'indexes': ['return_time', 'deadline']}

