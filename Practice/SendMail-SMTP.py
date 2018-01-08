#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):  # 格式化一个邮件地址
    name, addr = parseaddr(s)  # parseaddr()解析邮件地址
    return formataddr((Header(name, 'utf-8').encode(), addr))
    # 如果包含中文，需要通过Header对象进行编码


from_addr = input('From: ')
password = input('Password: ')
to_addr = input('To: ')
smtp_server = input('SMTP server (eg: smtp.263xmail.com): ')

# from_addr = 'ynlong@cienet.com.cn'
# password = '******'
# to_addr = 'ynlong@cienet.com.cn'
# smtp_server = 'smtp.263xmail.com'

msg = MIMEText('<html><body><h1>你好，我是Long Yeni，这个是我通过python发送的邮件</h1>' + '<p><a href="https://github.com/join/plan">这是一个多媒体内容</a></p>' + '</body></html>', 'html', 'utf-8')
msg['From'] = _format_addr('发送 <%s>' % from_addr)
msg['To'] = _format_addr('接收 <%s>' % to_addr)
msg['Subject'] = Header('我是Long Yeni，这个是我通过python发送的邮件', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
# server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息,打开或关闭调试信息
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
# as_string()把MIMEText对象变成str
server.quit()
