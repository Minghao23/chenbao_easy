# -*- coding: utf-8 -*-
import server
import loggers
import requests
import json
import os
from ConfigParser import ConfigParser

logger = loggers.get_logger()

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
conf = ConfigParser()
conf.read(os.path.join(root_dir, 'chenbao/features/coolq_apis/config.ini'))

api_key = conf.get('tuling', 'api_key')


def req_tuling(msg):
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": "001"
        }
    }

    r = requests.post(url, data=json.dumps(data))
    results = r.json()['results']
    for result in results:
        if result['resultType'] == 'text':
            return result['values']['text']
    raise RuntimeError('Error')


def baidu_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % \
          (conf.get('baidu_unit', 'api_key'), conf.get('baidu_unit', 'api_secret'))
    r = requests.get(url)
    return r.json()['access_token']


def req_baidu(msg):
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token
    data = {
        'log_id': 'UNITTEST_10000',
        'version': '2.0',
        'service_id': 'S10000',
        'session_id': '',
        'request': {
            'query': msg,
            'user_id': '001'
        },
        'dialog_state': {
            'contexts': {
                'SYS_REMEMBERED_SKILLS': ['1057']
            }
        }
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response:
        print (response.json())


def reply(msg, **kwargs):
    from client import send_group_msg
    logger.info("Received question: %s" % msg)

    if msg in ['帮助']:
        send_group_msg("关键字：\n"
                       "「帮助」—— 查看帮助信息\n"
                       "「还有谁」—— 未发晨报人员查询\n"
                       "「提醒」—— @所有未发晨报人员\n"
                       "「排行」—— 最近一个月发报排行榜\n"
                       "「统计」—— 统计最近一个月发报情况\n")

    elif msg in ['还有谁', '未发晨报']:
        chenbao_list = server.get_chenbao_list()
        remainings_qq = server.find_remainings_qq(chenbao_list)
        if len(remainings_qq) == 0:
            send_group_msg('book思议！所有人都已经发晨报了哦！')
            return
        remainings_name = []
        for qq in remainings_qq:
            remainings_name.append(server.staffs[str(qq)])
        send_group_msg('还有 %d 个人没发晨报，也不知道他们还发不发[CQ:face,id=179]\n\n%s' %
                       (len(remainings_name), ' '.join(remainings_name)))

    elif msg in ['提醒']:
        from client import msg_notify_remainings
        chenbao_list = server.get_chenbao_list()
        remainings_qq = server.find_remainings_qq(chenbao_list)
        if len(remainings_qq) == 0:
            send_group_msg('book思议！所有人都已经发晨报了哦！')
            return
        msg_notify_remainings(remainings_qq)

    elif msg in ['统计']:
        from chenbao.views import total_stat_helper
        import datetime
        datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
        datetime_start = datetime_now - datetime.timedelta(days=31)
        datetime_end = datetime_now - datetime.timedelta(days=1)
        dct = {"start_date": datetime_start.strftime('%Y%m%d'), "end_date": datetime_end.strftime('%Y%m%d')}
        res = total_stat_helper(dct)
        text = ['【近30日晨报发送时间统计】']
        text.append('平均发报时间: %s（于周期内呈%s）' % (res['total_avg'], res['trend']))
        text.append('日均发报时间最早员工: %s（比平均时间%s）' % (res['earliest_person'], res['earliest_diff']))
        text.append('日均发报时间最晚员工: %s（比平均时间%s）' % (res['latest_person'], res['latest_diff']))
        text.append('更多详情 http://192.168.1.160:8012/TotalStat ')
        send_group_msg('\n'.join(text))

    elif msg in ['排行榜', '排行', 'rank']:
        from chenbao.views import stat_rank
        import datetime
        datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
        datetime_start = datetime_now - datetime.timedelta(days=31)
        datetime_end = datetime_now - datetime.timedelta(days=1)
        dct = {"start_date": datetime_start.strftime('%Y%m%d'), "end_date": datetime_end.strftime('%Y%m%d')}
        rank = stat_rank(dct)
        text = ['【近30日晨报发送时间 TOP-10】']
        text.append(' （%s - %s）' % (datetime_start.strftime('%y.%m.%d'), datetime_end.strftime('%y.%m.%d')))
        text.append('------------------------------------')
        for i, item in enumerate(rank):
            t = '{0:<2}  {1:<6}   {2:>8}'.format(i + 1, item[0], item[1])
            text.append(str(t))
        text.append('------------------------------------')
        text.append('更多详情 http://192.168.1.160:8012/TotalStat')
        send_group_msg('\n'.join(text))

    elif msg == '你好':
        if 'qq' in kwargs and kwargs['qq'] == '751948630':
            send_group_msg('你好，我是你爸爸[CQ:face,id=14]')
        else:
            send_group_msg('你好，我是可爱的晨报易小助手——小易，请问有什么可以帮助您的呢~[CQ:face,id=21]')

    else:
        try:
            ans = req_tuling(msg)
            send_group_msg(ans)
        except Exception:
            import traceback
            logger.info(traceback.format_exc())
            send_group_msg('小易没有听懂你的问题，需要人工服务请@胡明昊，谢谢')
