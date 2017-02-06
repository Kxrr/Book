聘宝藏经阁
=========

基于 Flask 与 MongoDB 的内部图书借阅管理系统

[book.pinbot.me](http://book.pinbot.me/)

## 理念

将个人私有和公司的图书信息整合到一起

## 特性

- 本地用户系统
- 使用豆瓣、京东链接添加图书到应用中
- 借书还书
- 搜索
- 评论系统
- 用户活跃排行榜
- 邮件通知系统

## 部署说明

- 安装依赖: `pip install -r requirements.txt`
- 配置: 参照 `config_example.py` 建立 `config.py` 文件, 参照 `uwsgi_example.ini` 建立 `uwsgi.ini` 文件
- 运行应用:
    - simple server: `python manager.py runserver`
    - 使用 uwsgi: `uwsgi --ini uwsgi.ini`


