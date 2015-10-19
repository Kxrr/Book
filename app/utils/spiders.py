#-*- coding: utf-8 -*-

import requests
from lxml import etree
from app.models import BookInfo, User


class BasicSpider(object):
    def __init__(self, url, owner_id, online_url=''):
        self.url = url
        self.owner_id = owner_id
        self.online_url = online_url
        self.content = ''
        self.html = ''
        self.new_book = ''

        self.title = ''
        self.author = ''
        self.rate = 0.0
        self.img_url = ''
        self.detail = ''
        self.tags = []
        self.category = ''

    def crawl(self):
        self.content = requests.get(self.url).content
        self.html = etree.HTML(self.content)

    def save(self):
        self.new_book = BookInfo(title=self.title, author=self.author, rate=self.rate,
                                 detail=self.detail, tags=self.tags, category=self.category,
                                 raw_url=self.url, online_url=self.online_url, img_url=self.img_url).save()
        return self.new_book


class JdSpider(BasicSpider):
    """
    http://book.jd.com/
    """
    pass


class DoubanSpider(BasicSpider):
    def parse_content(self):
        title = self.html.xpath('//h1/span/text()')
        if title:
            self.title = title[0]

        author = self.html.xpath('//div[@id="info"]//a/text()')
        if author:
            self.author = author[0]

        rate = self.html.xpath('//div[@class="rating_wrap"]//strong/text()')  # float
        if rate:
            self.rate = float(rate[0])

        img_url = self.html.xpath('//div[@class="article"]//a[@class="nbg"]/img/@src')
        if img_url:
            self.img_url = img_url[0]

        self.detail = self.html.xpath('//div[@class="intro"]/p/text()')  # paragraph, lists
        self.tags = self.html.xpath('//div[@class="indent"]/span/a/text()')  # lists
        if not BookInfo.objects(title=self.title, author=self.author):
            new_book = self.save()
            new_book.update(push__owner=User.objects.get(id=self.owner_id))
            User.objects(id=self.owner_id).first().update(push__owned_book=self.new_book)
            return True
        else:
            exist_book = BookInfo.objects(title=self.title).first()
            add_book = exist_book.update(push__owner=User.objects.get(id=self.owner_id), inc__num=1)
            User.objects(id=self.owner_id).first().update(push__owned_book=exist_book)
            return True


class DoubanReadSpider(BasicSpider):
    def parse_content(self):
        title = self.html.xpath('//h1[@class="article-title"]/text()')
        if title:
            self.title = title[0]

        author = self.html.xpath('//a[@class="author-item"]/text()')
        if author:
            self.author = author[0]

        rate = self.html.xpath('//span[@class="rating-average"]/text()')
        if rate:
            self.rate = float(rate[0])

        img_url = self.html.xpath('//div[@class="cover shadow-cover"]/img/@src')
        if img_url:
            self.img_url = img_url[0]

        self.detail = self.html.xpath('//div[@class="article-profile-section article-profile-intros"]//p/text()')
        self.tags = self.html.xpath('//*[@class="tags"]//span[1]/text()')
        self.category = ''

        if not BookInfo.objects(title=self.title, author=self.author):
            new_book = self.save()
            new_book.update(push__owner=User.objects.get(id=self.owner_id))
            User.objects(id=self.owner_id).first().update(push__owned_book=new_book)
            return True
        else:
            exist_book = BookInfo.objects(title=title)
            add_book = exist_book.update(push__owner=User.objects.get(id=self.owner_id), inc__num=1)
            User.objects(id=self.owner_id).first().update(push__owned_book=exist_book.first())
            return True


