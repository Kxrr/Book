#-*- coding: utf-8 -*-
from flask import render_template, redirect, flash, request
from app.models import BookInfo, User, Delivery, Comment
from . import detail
from flask.ext.login import current_user, login_required


@detail.route('/Detail/<string:book_id>')
def book_detail(book_id):
    book_obj = BookInfo.objects(id=book_id).first()
    delivers = Delivery.objects(book=book_obj)
    return render_template('detail.html', book=book_obj, delivers=delivers)


@detail.route('/handle_comment', methods=['POST'])
@login_required
def handle_comment():
    form = request.form
    content = request.form['content']
    book_id = request.form['book_id']
    user = User.objects(id=current_user.id).first()
    book = BookInfo.objects(id=book_id).first()
    comment = Comment(content=content, name=user)
    book.update(push__comment=comment)
    flash(u'评论成功')
    return redirect('/Detail/{}'.format(book_id))