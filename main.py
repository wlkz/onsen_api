# coding=utf-8

import requests as re
import time
import logging
import json

from config import *


def parser(s):
    return json.loads(s[9:-3])


def fetch_source():
    try:
        req = re.get(REQUEST_URL)
        json_data = parser(req.text)
    except Exception as e:
        logging.info('a error occurred while fetching')
        return None
    logging.info('fetch success')
    return json_data


def send_mail(data):
    from email.header import Header
    from email.mime.text import MIMEText
    from email.utils import parseaddr, formataddr

    import smtplib

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    
    template = """
    <p>您订阅的节目已经更新。<br>
    标题：{}<br>
    回数：{}<br>
    更新日期：{}<br>
    更新信息：{}<br>
    下载地址：<a href="{}">点击下载</a></p>
    """.format(
        data['title'],
        data['count'],
        data['update'],
        data['schedule'],
        data['moviePath']['pc']
    )

    

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    server.starttls() #Puts connection to SMTP server in TLS mode
    server.ehlo()
    server.login(from_addr, password)
    for to_addr in to_addrs:
        msg = MIMEText(template, 'html', 'utf-8')
        msg['From'] = _format_addr(from_addr)
        msg['To'] = _format_addr(to_addr)
        if DEBUG:
            msg['Subject'] = Header('【测试】 {} 更新告知'.format(data['title']), 'utf-8').encode()
        else:
            msg['Subject'] = Header('{} 更新告知'.format(data['title']), 'utf-8').encode()
        server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def listen():
    REQUEST_URL = REQUEST_PREFIX + PROGRAM_NAME
    logging.info('start listening...')
    first_fetch = True
    while True:
        json_data = fetch_source()
        if not json_data:
            continue
        if first_fetch:
            logging.info('first fetch success')
            logging.info('title:{}'.format(json_data['title']))
            logging.info('count:{}'.format(json_data['count']))
            count = int(json_data['count'])
            first_fetch = False
        else:
            if DEBUG:
                count = -1
            if count < int(json_data['count']):
                count = int(json_data['count'])
                logging.info('source updateed, count:{}'.format(
                    json_data['count']))
                logging.info('sending mail')
                send_mail(json_data)
            else:
                logging.info('count:{}'.format(json_data['count']))
                logging.info('seems nothing update')
        logging.info('wait for the next fetch')
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    try:
        listen()
    except KeyError:
        logging.info('seems api have changed..')

