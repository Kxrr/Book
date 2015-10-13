#-*- coding: utf-8 -*

from app import app
from flask import render_template, request, redirect, url_for
from models import SpiderForm, BookInfo

from untils.spiders import DoubanSpider, JdSpider


@app.route('/')
def hello():
    form = SpiderForm()
    Spiders = BookInfo.objects
    return render_template('index.html', form=form, Spiders=Spiders)

@app.route('/add_from_url', methods=['POST'])
def add_from_url():
    form = SpiderForm(request.form)
    raw_url = form.raw_url.data
    if 'douban' in raw_url:
        DoubanSpider(raw_url).start()
        return ''
    elif 'jd' in raw_url:
        JdSpider(raw_url).start()
        return ''
    else:
        return 'Wrong!'
