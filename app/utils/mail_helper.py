# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib

"""
notif = Email.mailhelper()
notif.send('sub', 'content')
- 2015年7月9日
"""

class mailhelper(object):
    def __init__(self):
        self.mail_host="smtp.sina.com"  #设置服务器
        self.mail_user="random009s"    #用户名
        self.mail_pass="randomemail"   #密码
        self.mail_postfix="sina.com"  #发件箱的后缀


    def send(self, sub, content):
        to_list=['imres@qq.com']
        me="Alarm"+"<"+self.mail_user+"@"+self.mail_postfix+">" #自己的称呼
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False
