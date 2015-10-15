#-*- coding: utf-8 -*-

import requests
from lxml import etree
from app.models import BookInfo

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
    def __init__(self, url):
        self.url = url

    def start(self):
        self.content = requests.get(self.url).content

    def scrub_content(self):
        html = etree.HTML(self.content)
        title = html.xpath('//h1/span/text()')[0]
        try:
            author = html.xpath('//div[@id="info"]//a/text()')[0]
        except:
            author=''
            pass # TODO:
        rate = float(html.xpath('//div[@class="rating_wrap"]//strong/text()')[0])  # float
        detail = html.xpath('//div[@class="intro"]/p/text()')  # paragraph, lists
        tags = html.xpath('//div[@class="indent"]/span/a/text()')  # lists
        category = ''
        raw_url = self.url

        BookInfo(title=title, author=author, rate=rate, detail=detail, tags=tags, category=category, raw_url=raw_url).save()



# d = DoubanSpider('http://book.douban.com/subject/25909313/?icn=index-editionrecommend')
# d.start()
# d.scrub_content()
