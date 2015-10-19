#-*- coding: utf-8 -*-                                                                                     

from app.models import BookInfo

def search(keyword):
    try:
        keyword = keyword.decode('utf-8')
    except UnicodeEncodeError:
        pass
    finally:
        result = []
        s_title = BookInfo.objects(title__icontains=keyword)
        s_author = BookInfo.objects(author__icontains=keyword)
        s_tags = BookInfo.objects(tags__contains=keyword)
        result += s_title
        result += s_author
        result += s_tags
        result = list(set(result))
        return result

