#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg, n=0):
    if n == 0:
        for header in ['Subject', 'From', 'To', 'Cc']:
            value = msg.get(header, '')
            if header == 'Subject':
                value = decode_str(value)
            if header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
            if header == 'To' or header == 'Cc':
                L = value.split(',')
                value = []
                for x in L:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    x = u'%s <%s>' % (name, addr)
                    value.append(x)
            print('%s: %s' % (header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print_info(part, n + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('Text: %s' % content)
        else:
            print('Attachment: %s' % content_type)


email = input('Email: ')
password = input('Password: ')
pop3_server = input('POP3 server (eg: pop3.263xmail.com): ')


# email = 'ynlong@cienet.com.cn'
# password = '******'
# pop3_server = 'pop3.263xmail.com'

server = poplib.POP3(pop3_server)
# server.set_debuglevel(1)  # 打开或关闭调试信息
server.user(email)
server.pass_(password)
resp, mails, octets = server.list()  # list()返回所有邮件的编号
index = len(mails)  # 获取最新一封邮件编号
resp, lines, octets = server.retr(index)  # retr()获取邮件内容
msg_content = b'\r\n'.join(lines).decode('utf-8')  # 获得整个邮件的原始文本
msg = Parser().parsestr(msg_content)  # 把邮件内容解析为Message对象
server.quit()
print_info(msg)
