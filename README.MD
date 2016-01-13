Book Room
=========
基于Flask与MongoDB的内部图书借阅管理系统

## 理念
将个人和公司的图书信息整合到一起，形成良好的分享氛围

## 特性
1. 本地用户系统
2. 从豆瓣添加图书
3. 借书还书
4. 搜索
5. 简单过滤
6. 用户之间数据互通
7. 评论社交
8. 行为监测
9. 排行榜
10. 邮件通知系统

## 部署

#### 安装MongoDB
https://docs.mongodb.org/manual/administration/install-on-linux/

#### 安装Pypi
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
```

配置国内数据源 ~/.pip/pip.conf
```
[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com
```
#### 使用VirtualenvWrapper管理虚拟环境
```
$ pip install virtualenvwrapper
```
修改.bashrc
```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
   export WORKON_HOME=$HOME/.virtualenvs
   source /usr/local/bin/virtualenvwrapper.sh
fi
```
再次读入.bashrc:
```
$ source ~/.bashrc
```

#### 具体应用
1. 建立虚拟环境：`$ mkvirtualenv bookroom`
2. 进入bookroom：`$ workon bookroom`
3. 安装依赖包：`$ pip install –r requirements.txt`
4. 设置环境： `$ export PYTHONPATH=$(pwd)`
5. 运行: `$ python manager.py runserver -d`