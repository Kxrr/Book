#-*- coding: utf-8 -*-
"""
数目owner排序,借阅数排序,数目借阅量排序,简单处理为从系统开始运行后sum.
"""

from app.models import User, BookInfo, Delivery


def count_owned():  # 统计有贡献最多图书的人
    name = []
    count = []
    for user in User.objects:
        name.append(user.nickname)
        count.append(len(user.owned_book))
    result = zip(name, count)
    result_sorted = sorted(result, key=lambda x: x[1], reverse=True)
    return result_sorted


def count_borrowed():  # 统计借过最多书的人
    name = []
    count = []
    for user in User.objects:
        name.append(user.nickname)
        count.append(Delivery.objects(user=user).count())
    result = zip(name, count)
    result_sorted = sorted(result, key=lambda x: x[1], reverse=True)
    return result_sorted


def count_pop_book():  # 统计最受欢迎的图书
    book_name = []
    count = []
    for book in BookInfo.objects:
        book_name.append(book.title)
        count.append(Delivery.objects(book=book).count())
        result = zip(book_name, count)
        result_sorted = sorted(result, key=lambda x: x[1], reverse=True)
    return result_sorted


if __name__ == '__main__':
    count_pop_book()
