#-*- coding: utf-8 -*-

from app import app
app.debug = True
app.run(port=5321)


# TODO:
# 1. 搜索后没有逻辑处理
# 2. 借阅后'想读'选项