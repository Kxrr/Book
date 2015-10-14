#-*- coding: utf-8 -*-

import requests
from lxml import etree

class JdSpider(object):

    def __init__(self, url):
        self.url = url
        print 'Douban initiating...'

    def start(self):
        self.content = requests.get(self.url).content



class DoubanSpider(object):

    def __init__(self, url):
        self.url = url
        print 'Douban initiating...'

    def start(self):
        self.content = requests.get(self.url).content

    def sort_content(self):
        html = etree.HTML(self.content)
        title = html.xpath('//h1/span/text()')
        author = html.xpath('//div[@id="info"]//a/text()')
        rate = html.xpath('//div[@class="rating_wrap"]//strong/text()')


