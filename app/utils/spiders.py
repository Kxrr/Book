#-*- coding: utf-8 -*-

import requests
from lxml import etree
from app.models import BookInfo
from flask.ext.login import current_user

class JdSpider(object):
    """
    http://book.jd.com/
    """
    def __init__(self, url):
        self.url = url

    def start(self):
        self.content = requests.get(self.url).content



class DoubanSpider(object):
    """
    TODO: http://read.douban.com/ebook/1120350/?dcs=book-search
    """
    def __init__(self, url, owner=''):
        self.url = url
        self.owner = owner

    def start(self):
        self.content = requests.get(self.url).content

    def scrub_content(self):
        html = etree.HTML(self.content)
        try:
            title = html.xpath('//h1/span/text()')[0]
        except:
            title = ''
        try:
            author = html.xpath('//div[@id="info"]//a/text()')[0]
        except:
            author = ''
            pass
        try:
            rate = float(html.xpath('//div[@class="rating_wrap"]//strong/text()')[0])  # float
        except:
            rate = 0
        # TODO: remove try
        detail = html.xpath('//div[@class="intro"]/p/text()')  # paragraph, lists
        tags = html.xpath('//div[@class="indent"]/span/a/text()')  # lists
        category = ''  # TODO:

        BookInfo(title=title, author=author, rate=rate, detail=detail, tags=tags,
                 category=category, raw_url=self.url, owner=self.owner).save()



# d = DoubanSpider('http://book.douban.com/subject/25909313/?icn=index-editionrecommend')
# d.start()
# d.scrub_content()
