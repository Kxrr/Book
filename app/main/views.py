#-*- coding: utf-8 -*


from flask import render_template, redirect, flash, request
from app.models import BookInfo, User, Operation, Delivery
from . import main
from flask.ext.login import current_user, login_required

from app.utils import amount_fake_aggregation
from app.utils.search_mongo import search

page_limit = 60


@main.route('/')
def index(category=''):
    category_dict = {
        'category': category
    }
    book_count = BookInfo.objects.count()
    if category:
        books = BookInfo.objects.filter(**category_dict)
    else:
        books = BookInfo.objects.limit(page_limit)
    users = User.objects
    book_amount = amount_fake_aggregation.count_all()
    book_out = Delivery.objects(returned__ne=True).count()
    return render_template('index.html', books=books, user=current_user, all_books=books,
                           users=users, page=(book_count/page_limit)+2, current_page=1,
                           book_amount=book_amount, book_out=book_out)


@main.route('/page/<string:n>')
def index_page(n):
    # TODO: 分页实现的优化
    skip = (int(n)-1) * page_limit
    book_count = BookInfo.objects.count()
    books = BookInfo.objects.skip(skip).limit(page_limit)
    users = User.objects
    book_amount = amount_fake_aggregation.count_all()
    book_out = Delivery.objects(returned__ne=True).count()
    return render_template('index.html', books=books, user=current_user, all_books=books, users=users,
                           page=(book_count/page_limit)+2, current_page=int(n),
                           book_amount=book_amount, book_out=book_out)


@main.route('/borrow_book/<string:book_id>')
@login_required
def borrow_book(book_id):
    if current_user.is_active:
        book_obj = BookInfo.objects(id=book_id).first()
        user_online_obj = User.objects(id=current_user.id).first()  # Watch out, current_user is <class 'werkzeug.local.LocalProxy'>
        if (book_obj not in user_online_obj.borrowed_book) and (book_obj.num > 0):
            book_obj.update(dec__num=1, push__user_borrowed=user_online_obj)
            user_online_obj.update(push__borrowed_book=book_obj)

            Operation(type='borrow', user=user_online_obj, book_info=book_obj).save()
            Delivery(user=user_online_obj, book=book_obj).save()
            # 异常处理
            flash(u'「{}」, 借阅成功'.format(book_obj.title))
        else:
            flash(u'失败, 同一本书每人只能借一本')
    else:
        flash(u'失败, 请登录后再操作')
    return redirect('/')


@main.route('/want_book/<string:book_id>')
@login_required
def want_book(book_id):
    book = BookInfo.objects.get(id=book_id)
    user = User.objects.get(id=current_user.id)
    user.update(push__wanted_book=book)
    flash(u'「{}」, 收藏成功, 有书时会发送邮件通知(其实目前还没有)'.format(book.title))
    return redirect('/')


@main.route('/pull_want_book/<string:book_id>')
@login_required
def pull_want_book(book_id):
    book = BookInfo.objects.get(id=book_id)
    user = User.objects.get(id=current_user.id)
    user.update(pull__wanted_book=book)
    flash(u'「{}」, 取消收藏成功'.format(book.title))
    return redirect('/')


@main.route('/Search', methods=['POST'])
def handle_search():
    keyword = request.form['keyword'].strip()
    results = search(keyword)
    return render_template('search_result.html', results=results, keyword=keyword, user=current_user)


@main.route('/filter/on_bookshelf')
def filter_shelf():
    all_books = BookInfo.objects
    books = all_books.filter(num__gt=0)
    users = User.objects
    return render_template('index.html', books=books, user=current_user, all_books=all_books, users=users, page=1)

@main.route('/category/<string:category>')
def filter_category(category):
    return index(category=category)



# @main.route('/redirect/<url>')
# def redirect_url(url):
#     print url
#     if 'http' in url:
#         return redirect(url)
#     else:
#         return redirect('http://' + url)


@main.route('/test_1')
@login_required
def test_1():
    return '--'


@main.errorhandler(401)
def un_authorized(e):
    flash(u'此操作需要登录')
    return redirect('/Login')



