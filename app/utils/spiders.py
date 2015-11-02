#-*- coding: utf-8 -*-

import requests
from lxml import etree
from app.models import BookInfo, User


class BasicSpider(object):
    def __init__(self, url, owner_id, online_url=''):
        self.url = url.strip()
        self.owner_id = owner_id
        self.online_url = online_url
        self.content = ''
        self.html = ''
        self.new_book = ''
        self.existed_book = ''

        self.content_dict = {}

    def crawl(self):
        self.content = requests.get(self.url).content
        self.html = etree.HTML(self.content)

    def if_exist_book(self):
        self.existed_book = BookInfo.objects(title=self.content_dict.get('title'),
                                             author=self.content_dict.get('author'))
        if self.existed_book:
            # 己经有这本书了
            return True
        else:
            return False

    def save(self):
        if self.content_dict.get('title'):
            self.new_book = BookInfo(**self.content_dict).save()
            self.new_book.update(push__owner=User.objects.get(id=self.owner_id))
            User.objects(id=self.owner_id).first().update(push__owned_book=self.new_book)
            return self.new_book
        else:
            return False

    def save_with_existed(self):
        if self.if_exist_book():
            self.existed_book.update(push__owner=User.objects.get(id=self.owner_id), inc__num=1)
            print self.existed_book
            User.objects(id=self.owner_id).first().update(push__owned_book=self.existed_book.first())
            return True
        else:
            return self.save()


class DoubanSpider(BasicSpider):
    def parse_content(self):
        title = self.html.xpath('//h1/span/text()')
        author = self.html.xpath('//div[@id="info"]//a/text()')
        rate = self.html.xpath('//div[@class="rating_wrap"]//strong/text()')  # float
        img_url = self.html.xpath('//div[@class="article"]//a[@class="nbg"]/@href')
        detail = self.html.xpath('//div[@class="intro"]/p/text()')  # paragraph, list
        tags = self.html.xpath('//div[@class="indent"]/span/a/text()')  # list

        self.content_dict = {
            'title': title[0] if title else '',
            'author': author[0] if author else '',
            'rate': float(rate[0].strip()) if (rate and '.' in rate[0]) else 0,
            'detail': detail if detail else [],
            'tags': tags if len(tags) < 5 else tags[0:5],
            'raw_url': self.url,
            'online_url': self.online_url,
            'img_url': img_url[0] if img_url else '',
        }

        return self.save_with_existed()


class JingDongSpider(BasicSpider):
    def parse_content(self):
        title = self.html.xpath('//div[@id="name"]/h1/text()')
        author = self.html.xpath('//div[@id="name"]/div[@id="p-author"]/a/text()')
        img_url = self.html.xpath('//div[@id="preview"]//img/@src')
        detail = self.html.xpath('//div[@class="book-detail-item"]/div[@class="item-mc"]/div[@class="book-detail-content"]/p/text()')  # paragraph, list

        self.content_dict = {
            'title': title[0] if title else '',
            'author': author[0] if author else '',
            'detail': detail if detail else [],
            'raw_url': self.url,
            'online_url': self.online_url,
            'img_url': img_url[0] if img_url else '',
        }

        return self.save_with_existed()
