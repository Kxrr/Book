#-*- coding: utf-8 -*

from mongoengine import DynamicDocument, EmbeddedDocument, connect, StringField, ListField, FloatField, \
    DateTimeField, BooleanField, ReferenceField, EmbeddedDocumentField, IntField, queryset_manager
from datetime import datetime, timedelta

connect('BookRoom')


class User(DynamicDocument):
    username = StringField(max_length=20, unique=True, required=True, min_length=4)
    email = StringField(unique=True)
    password = StringField(required=True, min_length=6)
    nickname = StringField(min_length=1)
    real_name = StringField()
    borrowed_book = ListField(ReferenceField('BookInfo'))
    role = StringField(default='staff')
    owned_book = ListField(ReferenceField('BookInfo'))
    wanted_book = ListField(ReferenceField('BookInfo'))  # 没有书时的收藏功能

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Watch out here, needs str

    def save(self, *args, **kwargs):
        if not self.real_name:
            self.real_name = self.nickname
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.username

    meta = {'ordering': ['+nickname']}


class Comment(EmbeddedDocument):
    """
    @summary: 用户评论
    """
    content = StringField()
    name = ReferenceField(User)
    time = DateTimeField(default=datetime.now())
    meta = {'ordering': ['-time', '-id']}


class BookInfo(DynamicDocument):
    """
    @summary: 书的信息
    """
    title = StringField(unique=True)
    author = StringField()
    rate = FloatField()
    detail = ListField(StringField())
    tags = ListField(StringField())
    category = StringField()
    raw_url = StringField()
    online_url = StringField()
    img_url = StringField()
    update_time = DateTimeField(default=datetime.now())
    # on_bookshelf = BooleanField(default=True)
    deleted = BooleanField(default=False)  # 方便实现删除图书操作
    num = IntField(default=1)  # 书籍数量, 就对多本相同书属于不同的人
    owner = ListField(ReferenceField(User))  # 同上

    user_borrowed = ListField(ReferenceField(User))  # 哪些人正在借

    comment = ListField(EmbeddedDocumentField(Comment))

    meta = {'ordering': ['-update_time', '-id']}

    def __unicode__(self):
        return self.title

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.filter(deleted__ne=True)


class Operation(DynamicDocument):
    """
    @summary: 记录每一次操作, 不到万不得以不调用
    """
    type = StringField()
    user = ReferenceField(User)
    time = DateTimeField(default=datetime.now())
    book_info = ReferenceField(BookInfo)
    note = StringField()

    url_info = StringField()
    meta = {'oddering':['-time', '-id']}


class Delivery(DynamicDocument):
    """
    @summary: 书籍记录和归还时间, 采用单条文档的方式
    """
    borrow_time = DateTimeField(default=datetime.now())
    deadline = DateTimeField(default=datetime.now() + timedelta(days=30))  # 设置一个月后归还

    user = ReferenceField(User)
    book = ReferenceField(BookInfo)

    return_time = DateTimeField()
    returned = BooleanField(default=False)

if __name__ == '__main__':
    import ipdb; ipdb.set_trace()
    print ''