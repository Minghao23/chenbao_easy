# -*- coding: utf-8 -*-
import requests
import datetime
import json
import os
from ConfigParser import ConfigParser

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
conf = ConfigParser()
conf.read(os.path.join(root_dir, 'chenbao/features/coolq_apis/config.ini'))

group_id = conf.get('general', 'group_id')


def send_group_msg(msg):
    data = {
        'group_id': int(group_id),
        'message': msg,
        'auto_escape': False
    }

    api_url = 'http://127.0.0.1:5700/send_group_msg'

    r = requests.post(api_url, data=data)


def msg_send_email():
    send_group_msg('【晨报邮件已发送】[CQ:face,id=124][CQ:face,id=124][CQ:face,id=124]\n还没来得及发晨报的同学请自行转发邮件补发哦！\n有问题请随时@小易，性感小易在线解答！')


def msg_notify_remainings(remainings_qq):
    at_str = ''.join(['[CQ:at,qq=%s]' % qq for qq in remainings_qq])
    send_group_msg('%s\n\n小易提醒您发晨报了！截止时间下午4点哦！\n有问题请随时@小易，性感小易在线解答！' % at_str)


def msg_hello_to_all():
    datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
    today_str = datetime_now.strftime("%Y.%m.%d")
    dayofweeks = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    send_group_msg('============ %s %s 晨报分界线 ============' % (today_str, dayofweeks[datetime_now.weekday()]))
    send_group_msg('[CQ:face,id=212][CQ:face,id=212][CQ:face,id=212]')


def msg_error():
    send_group_msg('小易好像出了点问题，请联系最帅的@胡明昊小哥哥，谢谢！')


def get_group_list():
    data = {
        'group_id': int(group_id),
    }

    api_url = 'http://127.0.0.1:5700/get_group_member_list'

    r = requests.post(api_url, data=data)
    d = r.json()
    a = dict()
    for user in d['data']:
        if user['card'] != '':
            a[str(user['user_id'])] = user['card']
        else:
            a[str(user['user_id'])] = user['nickname']
    print(json.dumps(a))

