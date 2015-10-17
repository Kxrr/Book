#-*- coding: utf-8 -*


from flask import render_template, redirect, flash, request, url_for
from app.models import BookInfo, User, Operation, Delivery, Comment
from . import main
from flask.ext.login import current_user, login_required

from app.utils.search_mongo import search

page_limit = 7

@main.route('/')
def index():
    book_count = BookInfo.objects.count()
    books = BookInfo.objects.limit(page_limit)
    users = User.objects
    return render_template('index.html', books=books, user=current_user, all_books=books, users=users,
                           page=(book_count/page_limit)+2, current_page=1)

@main.route('/page/<string:n>')
def index_page(n):
    # TODO: 分页实现的优化
    skip = (int(n)-1) * page_limit
    book_count = BookInfo.objects.count()
    books = BookInfo.objects.skip(skip).limit(page_limit)
    users = User.objects
    return render_template('index.html', books=books, user=current_user, all_books=books, users=users,
                           page=(book_count/page_limit)+2, current_page=int(n))

@main.route('/borrow_book/<string:book_id>')
@login_required
def borrow_book(book_id):
    if current_user.is_active:
        book_obj = BookInfo.objects(id=book_id).first()
        user_online_obj = User.objects(id=current_user.id).first()  # Watch out, current_user is <class 'werkzeug.local.LocalProxy'>
        print type(user_online_obj)
        book_obj.update(set__on_bookshelf=False, user_borrowed=user_online_obj)
        user_online_obj.update(push__borrowed_book=book_obj)

        Operation(type='borrow', user=user_online_obj, book_info=book_obj).save()
        Delivery(user=user_online_obj, book=book_obj).save()

        # TODO: 设置归还时间 | done
        # 异常处理
        flash(u'「{}」, 借阅成功'.format(book_obj.title))
    else:
        flash(u'失败, 请登录后再操作')
    return redirect('/')


@main.route('/Detail/<string:book_id>')
def book_detail(book_id):
    book_obj = BookInfo.objects(id=book_id).first()
    delivers = Delivery.objects(book=book_obj)
    return render_template('detail.html', book=book_obj, delivers=delivers)


@main.route('/Search', methods=['POST'])
def handle_search():
    keyword = request.form['keyword'].strip()
    results = search(keyword)
    return render_template('search_result.html', results=results, keyword=keyword, user=current_user)

@main.route('/filter/on_bookshelf')
def filter_shelf():
    all_books = BookInfo.objects
    books = all_books.filter(on_bookshelf=True)
    users = User.objects
    return render_template('index.html', books=books, user=current_user, all_books=all_books, users=users, page=1)

@main.route('/handle_comment', methods=['POST'])
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


@main.route('/test_1')
@login_required
def test_1():
    return '--'

@main.errorhandler(401)
def un_authorized(e):
    flash(u'此操作需要登录')
    # return redirect(url_for('user.login')), 401
    return redirect('/Login')



