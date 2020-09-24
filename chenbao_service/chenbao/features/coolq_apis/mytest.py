# -*- coding: utf-8 -*-
import requests
from reply import req_tuling


def manually_sen_group_msg(group_id, host, msg):
    data = {
        'group_id': group_id,
        'message': msg,
        'auto_escape': False
    }

    api_url = 'http://%s:5700/send_group_msg' % host

    r = requests.post(api_url, data=data)


def manually_sen_private_msg(user_id, host, msg):
    data = {
        'user_id': user_id,
        'message': msg,
        'auto_escape': False
    }

    api_url = 'http://%s:5700/send_private_msg' % host

    r = requests.post(api_url, data=data)




# manually_sen_group_msg(629682055,
#                        '192.168.1.160',
#                        "[CQ:face,id=212]")


# manually_sen_private_msg(751948630, '192.168.1.160', 'haha')
