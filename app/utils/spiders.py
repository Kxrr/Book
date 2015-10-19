#-*- coding: utf-8 -*-

import requests
from flask import flash
from lxml import etree
from app.models import BookInfo, User
from mongoengine.queryset import NotUniqueError

class BasicSpider(object):
    def __init__(self, url, owner_id):
        self.url = url
        self.owner_id = owner_id
        self.content = ''
        self.html = ''

    def crawl(self):
        self.content = requests.get(self.url).content
        self.html = etree.HTML(self.content)


class JdSpider(BasicSpider):
    """
    http://book.jd.com/
    """
    pass

class DoubanSpider(BasicSpider):
    def parse_content(self):
        try:
            title = self.html.xpath('//h1/span/text()')[0]
        except:
            title = ''
        try:
            author = self.html.xpath('//div[@id="info"]//a/text()')[0]
        except:
            author = ''
            pass
        try:
            rate = float(self.html.xpath('//div[@class="rating_wrap"]//strong/text()')[0])  # float
        except:
            rate = 0
        # TODO: remove try
        detail = self.html.xpath('//div[@class="intro"]/p/text()')  # paragraph, lists
        tags = self.html.xpath('//div[@class="indent"]/span/a/text()')  # lists
        try:
            img_url = self.html.xpath('//div[@class="article"]//a[@class="nbg"]/img/@src')[0]
        except:
            img_url = ''
        category = ''  # TODO:
        if not BookInfo.objects(title=title, author=author):
            new_book = BookInfo(title=title, author=author, rate=rate, detail=detail, tags=tags,
                                category=category, raw_url=self.url,
                                img_url=img_url).save()
            new_book.update(push__owner=User.objects.get(id=self.owner_id))
            User.objects(id=self.owner_id).first().update(push__owned_book=new_book)
            return True
        else:
            exist_book = BookInfo.objects(title=title)
            add_book = exist_book.update(push__owner=User.objects.get(id=self.owner_id), inc__num=1)
            return True


class DoubanReadSpider(BasicSpider):
    def parse_content(self):
        title = self.html.xpath('//h1[@class="article-title"]/text()')[0]
        try:
            author = self.html.xpath('//a[@class="author-item"]/text()')[0]
        except:
            author = ''
        rate = float(self.html.xpath('//span[@class="rating-average"]/text()')[0])
        detail = self.html.xpath('//div[@class="article-profile-section article-profile-intros"]//p/text()')
        tags = self.html.xpath('//*[@class="tags"]//span[1]/text()')
        category = ''
        img_url = self.html.xpath('//div[@class="cover shadow-cover"]/img/@src')[0]
        try:
            new_book = BookInfo(title=title, author=author, rate=rate, detail=detail, tags=tags,
                     category=category, raw_url=self.url,
                     owner=User.objects.get(id=self.owner_id), img_url=img_url).save()
            User.objects(id=self.owner_id).first().update(push__owned_book=new_book)
            return True
        except NotUniqueError:
            flash(u'这本书己经添加过了')
            return False


