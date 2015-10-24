#-*- coding: utf-8 -*


from flask import render_template, redirect, flash, request
from app.models import BookInfo, User, Operation, Delivery
from . import main
from flask.ext.login import current_user, login_required

from app.utils import amount_fake_aggregation
from app.utils.email import send_fav_noti_to_owner,\
    send_fav_noti_to_borrowed, send_borrow_noti_to_owner
from app.utils.search_mongo import search


page_limit = 100


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
        book = BookInfo.objects(id=book_id).first()
        user = User.objects(id=current_user.id).first()
        if (book not in user.borrowed_book) and (book.num > 0):
            book.update(dec__num=1, push__user_borrowed=user)
            user.update(push__borrowed_book=book)
            Operation(type='borrow', user=user, book_info=book).save()
            Delivery(user=user, book=book).save()
            # 发送邮件给拥有者
            send_borrow_noti_to_owner(user, book.owner[0], book)
            flash(u'「{}」, 操作成功, 己经发送借阅通知邮件给拥有者 {}({})'
                  .format(book.title, book.owner[0].nickname, book.owner[0].real_name))
        else:
            flash(u'失败, 同一本书每人只能借一本')
    else:
        flash(u'请登录后再操作')
    return redirect('/')


@main.route('/want_book/<string:book_id>')
@login_required
def want_book(book_id):
    book = BookInfo.objects.get(id=book_id)
    user = User.objects.get(id=current_user.id)
    user.update(push__wanted_book=book)
    # 发送邮件给正在读的人
    send_fav_noti_to_borrowed(user, book.user_borrowed[0], book)
    # 发送邮件给拥者
    send_fav_noti_to_owner(user, book.owner[0], book)

    flash(u'「{}」, 收藏成功, 己经发送通知邮件给正在读这本书的 {}({})'
          .format(book.title, book.user_borrowed[0].nickname, book.user_borrowed[0].real_name))
    return redirect('/')


@main.route('/pull_want_book/<string:book_id>')
@login_required
def pull_want_book(book_id):
    book = BookInfo.objects.get(id=book_id)
    user = User.objects.get(id=current_user.id)
    user.update(pull__wanted_book=book)
    flash(u'「{}」, 取消收藏成功'.format(book.title))
    return redirect('/')


@main.route('/Search', methods=['POST', 'GET'])
def handle_search():
    if request.method == 'POST':
        keyword = request.form['keyword'].strip()
    else:
        keyword = request.args.get('keywords').strip()
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


@main.errorhandler(401)
def un_authorized(e):
    flash(u'此操作需要登录')
    return redirect('/Login')



