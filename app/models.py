#-*- coding: utf-8 -*

from mongoengine import *
from flask.ext.mongoengine.wtf import model_form
connect('BookRoom')

class BookInfo(DynamicDocument):
    raw_url = StringField()


SpiderForm = model_form(BookInfo)
