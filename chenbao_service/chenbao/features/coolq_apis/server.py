# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import re
import codecs
import json
import threading
import datetime
import pytz
import traceback
from ConfigParser import ConfigParser
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from threading import Timer
from loggers import get_logger

logger = get_logger()
mutex = threading.Lock()

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
conf = ConfigParser()
conf.read(os.path.join(root_dir, 'chenbao/features/coolq_apis/config.ini'))

tmp_chenbao_list_path = os.path.join(root_dir, 'data/tmp/tmp_chenbao_list.txt')
tmp_info_path = os.path.join(root_dir, 'data/tmp/tmp_info.json')

group_id = conf.get('general', 'group_id')
test_group_id = conf.get('general', 'test_group_id')

with codecs.open(os.path.join(root_dir, 'data/staffs_qq.json')) as f:
    staffs = json.load(f)['staffs']

# check tmp_info.json
if not os.path.exists(tmp_info_path):
    with open(tmp_info_path, 'w') as f:
        json.dump({'sent_email': False, 'last_send_email_date': None}, f)
else:
    with open(tmp_info_path, 'r') as f:
        info = json.load(f)
    if info['last_send_email_date'] is not None:
        datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
        today = datetime_now.strftime('%y%m%d')
        if today == info['last_send_email_date']:
            info['sent_email'] = True
    with open(tmp_info_path, 'w') as f:
        json.dump(info, f)


timers = []


def server(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['post_type'] == 'message':
            if data['message_type'] == 'group' and str(data['group_id']) in [group_id, test_group_id]:
                logger.info("Received message:\n%s" % data)
                reply(data)
                check_day_off(data)
                update_chenbao_list(data)
                check_and_send_email()
        return HttpResponse()


def already_sent_email():
    with mutex:
        with open(tmp_info_path, 'r') as f:
            info = json.load(f)

    return info['sent_email']


def reply(data):
    message_array = data['message']
    message_at = filter(lambda x: x['type'] == 'at', message_array)
    for at in message_at:
        if at['data']['qq'] == conf.get('general', 'bot_qq'):
            content = ''.join([msg['data']['text'].strip() if msg['type'] == 'text' else '' for msg in message_array])
            from chenbao.features.coolq_apis.reply import reply
            try:
                reply(content, qq=str(data['sender']['user_id']))
            except Exception:
                from chenbao.features.coolq_apis.client import msg_error
                msg_error()
            return


def check_day_off(data):
    message_array = data['message']
    content = ''.join([msg['data']['text'] if msg['type'] == 'text' else '' for msg in message_array])
    if content.startswith('[请假]'):
        absences = content.strip('[请假]').split(' ')
        good_absences = []
        bad_absences = []
        for absence in absences:
            absence = absence.strip()
            if absence == '':
                continue
            if absence in staffs.values():
                good_absences.append(absence)
            else:
                bad_absences.append(absence)
        if len(bad_absences) == 0:
            import codecs
            with codecs.open(os.path.join(root_dir, 'data/absent_persons.json'), 'r', encoding='utf-8') as f:
                dct = json.load(f)

            for good_absence in good_absences:
                if good_absence not in dct['absent_persons']:
                    dct['absent_persons'].append(good_absence)
            with codecs.open(os.path.join(root_dir, 'data/absent_persons.json'), 'w', encoding='utf-8') as f:
                json.dump(dct, f)
            ans = 'ok，已经把 %s 设置为请假状态了！' % ' '.join(good_absences)
        else:
            ans = '%s 不是我司员工哦' % ' '.join(bad_absences)

        from chenbao.features.coolq_apis.client import send_group_msg
        send_group_msg(ans)
        logger.info("Received day off message {%s}, and replied {%s}" % (content, ans))


def update_chenbao_list(data):
    """
    update temp chenbao list file, duplicate chenbao may occur in file due to repeated message
    """
    sender_qq = str(data['sender']['user_id'])
    message = data['message']
    timestamp = data['time']

    # check valid user_id
    if sender_qq not in staffs:
        return

    # only handle text message
    content = ''.join([msg['data']['text'] if msg['type'] == 'text' else '' for msg in message])

    # check valid name
    content = content.strip()
    content = content.strip(u'\u0010')
    if len(content) >= 2 and content[:2] in staffs.values():
        name = content[:2]
    elif len(content) >= 3 and content[:3] in staffs.values():
        name = content[:3]
    elif content[:9] == 'Catherine' or content[:9] == 'catherine':
        name = 'Catherine'
    else:
        return

    # a legal chenbao must have at least two lines
    if len(re.findall(re.compile(r'.*\n'), content)) == 0:
        return

    content = re.sub(re.compile(r'.*\n'), '', content, 1)

    time_datetime = datetime.datetime.utcfromtimestamp(timestamp) + datetime.timedelta(hours=8)  # China zone
    time_str = time_datetime.strftime('%H:%M:%S')

    with mutex:
        with open(tmp_chenbao_list_path, 'a') as f:
            f.write(json.dumps({'name': name, 'content': content, 'time': time_str}))
            f.write('\n')

    # if already sent chenbao today, do nothing
    if already_sent_email():
        from chenbao.features.coolq_apis.client import send_group_msg
        send_group_msg('小易提醒您，今天的晨报邮件已经发过了哟，请自行转发邮件补充。')


def check_and_send_email():
    # if already sent chenbao today, do nothing
    if already_sent_email():
        return

    chenbao_list = get_chenbao_list()
    remainings_qq = find_remainings_qq(chenbao_list)
    if len(remainings_qq) == 0:
        logger.info("All members have sent chenbao, send email after 2 min")
        if len(timers) != 0:
            timers[0].cancel()
            timers.pop(0)
        delay = int(conf.get('general', 'check_all_delay'))
        timer = Timer(delay, send_email, args=[chenbao_list])  # send email after 2min, avoid revert
        timer.start()
        timers.append(timer)


def send_email(chenbao_list):
    # if already sent chenbao today, do nothing
    if already_sent_email():
        return

    from chenbao.views import update_records
    from chenbao import mail
    from chenbao.features.coolq_apis.client import msg_send_email

    datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
    today_str = datetime_now.strftime("%Y%m%d")

    with codecs.open(os.path.join(root_dir, 'data/absent_persons.json'), 'r', encoding='utf-8') as f:
        absent_persons = json.load(f)['absent_persons']

    update_records(today_str, chenbao_list, len(absent_persons))

    subject = "北京晨会-%s" % today_str
    today_format_str = datetime_now.strftime("%Yn%my%dr")
    today_format_str = today_format_str.replace('n', '年').replace('y', '月').replace('r', '日')
    message = '\n\n'.join(['[%s]\n%s' % (chenbao['name'], chenbao['content']) for chenbao in chenbao_list])
    message = '\n发报日期：%s\n发报人数：%d\n请假人员：%s\n\n\n%s' % \
              (today_format_str, len(chenbao_list), ' '.join(absent_persons), message)

    mail.send_email(subject, message)
    msg_send_email()
    with mutex:
        with open(tmp_info_path, 'r') as f:
            info = json.load(f)
        datetime_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # China zone
        today = datetime_now.strftime('%y%m%d')
        info['sent_email'] = True
        info['last_send_email_date'] = today
        with open(tmp_info_path, 'w') as f:
            json.dump(info, f)
    logger.info("Successfully send email")


def get_chenbao_list():
    if not os.path.exists(tmp_chenbao_list_path):
        return []

    with mutex:
        with open(tmp_chenbao_list_path, 'r') as f:
            chenbao_str_list = f.readlines()
    chenbao_list = [json.loads(chenbao_str.strip('\n')) for chenbao_str in chenbao_str_list]

    # remove duplicates, keep latest
    visited = set()
    new_chenbao_list = list()
    for i in range(len(chenbao_list) - 1, -1, -1):
        if chenbao_list[i]['name'] in visited:
            continue
        new_chenbao_list.append(chenbao_list[i])
        visited.add(chenbao_list[i]['name'])

    new_chenbao_list.reverse()
    return new_chenbao_list


def find_remainings_qq(chenbao_list):
    with codecs.open(os.path.join(root_dir, 'data/absent_persons.json'), 'r', encoding='utf-8') as f:
        absent_persons = json.load(f)['absent_persons']
    good_persons = [x['name'] for x in chenbao_list]
    bad_persons = set(staffs.values()) - set(good_persons) - set(absent_persons)
    bad_persons_qq = []
    for qq, name in staffs.items():
        if name in bad_persons:
            bad_persons_qq.append(int(qq))
    return bad_persons_qq


def reset_tmp():
    with mutex:
        try:
            if os.path.exists(tmp_chenbao_list_path):
                # remove tmp_chenbao_list
                os.remove(tmp_chenbao_list_path)

            # set sent_email to False
            with open(tmp_info_path, 'r') as f:
                info = json.load(f)
            info['sent_email'] = False
            with open(tmp_info_path, 'w') as f:
                json.dump(info, f)

            # set absent_persons to []
            with codecs.open(os.path.join(root_dir, 'data/absent_persons.json'), 'w', encoding='utf-8') as f:
                json.dump({"absent_persons": []}, f)
            logger.info('Successfully reset.')

        except Exception:
            logger.error('Failed to reset. Details:\n%s' % traceback.format_exc())
            pass


def notify_remaining_persons():
    chenbao_list = get_chenbao_list()
    remainings_qq = find_remainings_qq(chenbao_list)
    if len(remainings_qq) > 0:
        from chenbao.features.coolq_apis.client import msg_notify_remainings
        msg_notify_remainings(remainings_qq)
        # logger.info("Remind of sending chenbao! for %s" % ' '.join(remainings_qq))


def hello_to_all():
    from chenbao.features.coolq_apis.client import msg_hello_to_all
    msg_hello_to_all()


def send_email_sched_task():
    # if already sent chenbao today, do nothing
    if already_sent_email():
        logger.info('Email has been sent before 4am, so do nothing.')
        return

    chenbao_list = get_chenbao_list()
    send_email(chenbao_list)


# set sched tasks
remind_days = conf.get('general', 'remind_days')
remind_hours = map(int, conf.get('general', 'remind_hours').split(','))
reset_hour = int(conf.get('general', 'reset_hour'))
hello_hour = int(conf.get('general', 'hello_hour'))
send_email_hour = int(conf.get('general', 'send_email_hour'))

scheduler = BackgroundScheduler()
for remind_hour in remind_hours:
    scheduler.add_job(notify_remaining_persons, 'cron', day_of_week=remind_days,
                      hour=remind_hour, minute=00, timezone=pytz.timezone('Asia/Shanghai')
                      , coalesce=True, misfire_grace_time=300)
scheduler.add_job(reset_tmp, 'cron',
                  hour=reset_hour, minute=00, timezone=pytz.timezone('Asia/Shanghai'),
                  coalesce=True, misfire_grace_time=300)  # reset everyday
scheduler.add_job(hello_to_all, 'cron', day_of_week=remind_days,
                  hour=hello_hour, minute=00, timezone=pytz.timezone('Asia/Shanghai')
                  , coalesce=True, misfire_grace_time=300)
scheduler.add_job(send_email_sched_task, 'cron', day_of_week=remind_days,
                  hour=send_email_hour, minute=00, timezone=pytz.timezone('Asia/Shanghai')
                  , coalesce=True, misfire_grace_time=300)
scheduler.start()
