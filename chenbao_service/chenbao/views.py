# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import re
import codecs
import os
import datetime
import mail
import loggers

logger = loggers.get_logger()

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

with codecs.open(os.path.join(root_dir, 'data/staffs.json')) as f:
    staffs = json.load(f)['staffs']


def get_init_data(request):
    if request.method == 'GET':
        with codecs.open('data/absent_persons.json') as f:
            absent_persons = json.load(f)['absent_persons']

        dct = {'staffs': staffs, 'absent_persons': absent_persons}
        response_json = json.dumps(dct, encoding='utf-8')

        return HttpResponse(response_json, content_type="application/json")


def update_absent_persons(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        with codecs.open('data/absent_persons.json', 'w', encoding='utf-8') as f:
            json.dump(dct, f)

        return HttpResponse()


def check_chat_content(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        chat_content = dct['chat_content']
        absent_persons = dct['absent_persons']

        chenbao_list = get_chenbao_list(chat_content)
        good_persons = [x['name'] for x in chenbao_list]
        bad_persons = set(staffs) - set(good_persons) - set(absent_persons)

        response_json = json.dumps({'remaining_persons': list(bad_persons)})

        return HttpResponse(response_json, content_type="application/json")


def generate_email(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        chat_content = dct['chat_content']
        absent_persons = dct['absent_persons']

        chenbao_list = get_chenbao_list(chat_content)

        today_str = datetime.datetime.now().strftime("%Y%m%d")
        update_records(today_str, chenbao_list, len(absent_persons))

        to = "; ".join(mail.To)
        cc = "; ".join(mail.Cc)
        subject = "北京晨会-%s" % today_str
        today_format_str = datetime.datetime.now().strftime("%Yn%my%dr")
        today_format_str = today_format_str.replace('n', '年').replace('y', '月').replace('r', '日')
        message = '\n\n'.join(['[%s]\n%s' % (chenbao['name'], chenbao['content']) for chenbao in chenbao_list])
        message = '\n发报日期：%s\n发报人数：%d\n请假人员：%s\n\n\n%s' % \
                  (today_format_str, len(chenbao_list), ' '.join(absent_persons), message)

        response_dict = {'to': to, 'cc': cc, 'subject': subject, 'message': message}
        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def send_email(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        subject = dct['subject']
        content = dct['content']
        rc = mail.send_email(subject, content)

        response_json = json.dumps({'rc': rc})
        return HttpResponse(response_json, content_type="application/json")


def get_chenbao_list(chat_content):
    pattern_header = re.compile(ur'\S*\s{2}\d{2}:\d{2}:\d{2}\n')
    pattern_recall = re.compile(ur'.*((撤回了一条消息)|(recalled a message)).*\n')
    pattern_change = re.compile(ur'.*((加入群)|(退出群)|(移出群))\n')

    with codecs.open(os.path.join(root_dir, 'data/staffs.json')) as f:
        staffs = json.load(f)["staffs"]

    out = re.sub(pattern_recall, "", chat_content)
    out = re.sub(pattern_change, "", out)
    cbs = re.split(pattern_header, out)
    if len(cbs) <= 1:
        return []
    cbs = cbs[1:]  # drop the first meaningless string
    cbs = map(lambda x: x[1:] if len(x) > 0 and x[0] == '\n' else x, cbs)  # remove \n suffix and prefix
    cbs = map(lambda x: x[:-1] if len(x) > 0 and x[-1] == '\n' else x, cbs)
    cb_times = re.findall(pattern_header, out)
    cb_times = map(lambda x: x[-9: -1], cb_times)
    assert len(cbs) == len(cb_times)

    chenbao_list = []  # why don't use dict? Cuz I want to keep the order of chenbaos
    chenbao_name_set = set()

    for i, cb in enumerate(cbs):
        cb = cb.strip()
        cb = cb.strip(u'\u0010')
        if len(cb) >= 2 and cb[:2] in staffs:
            name = cb[:2]
        elif len(cb) >= 3 and cb[:3] in staffs:
            name = cb[:3]
        elif cb[:9] == 'Catherine' or cb[:9] == 'catherine':
            name = 'Catherine'
        else:
            continue

        content = re.sub(re.compile(r'.*\n'), '', cb, 1)

        if name in chenbao_name_set:  # only keep the latest content for a person
            for i, chenbao in enumerate(chenbao_list):
                if chenbao['name'] == name:
                    chenbao_list[i]['content'] = content
                    break
        else:
            chenbao_list.append({'name': name, 'content': content, 'time': cb_times[i]})
            chenbao_name_set.add(name)

    return chenbao_list


def update_records(today_str, chenbao_list, absent_num):
    record_path = os.path.join(root_dir, 'data/records/%s.json' % today_str)
    record = dict(total_staff=len(staffs), absent=absent_num)
    if os.path.exists(record_path):
        with codecs.open(record_path) as f:
            old_record = json.load(f)
        old_chenbao_list = old_record['chenbao_list']
        new_chenbao_list = chenbao_list[:]
        chenbao_list_names = set([chenbao['name'] for chenbao in chenbao_list])
        for old_chenbao in old_chenbao_list:
            if old_chenbao['name'] not in chenbao_list_names:
                new_chenbao_list.append(old_chenbao)
        record['chenbao_list'] = new_chenbao_list
        with codecs.open(record_path, 'w', encoding='utf-8') as f:
            json.dump(record, f)
    else:
        record['chenbao_list'] = chenbao_list
        with codecs.open(record_path, 'w', encoding='utf-8') as f:
            json.dump(record, f)


def check_date(start_date_str, end_date_str):
    """
    Validate the date and handle the default case
    Only consider workday, say Mon - Fri
    :param start_date_str: YYYYMMDD string
    :param end_date_str: YYYYMMDD string
    :return: YYYYMMDD from start_date to end_date except weekends
    """
    if end_date_str is None:
        end_date = datetime.datetime.today()
    else:
        end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d")

    if start_date_str is None:
        start_date = end_date - datetime.timedelta(days=30)
    else:
        start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d")

    if start_date > end_date:
        raise ValueError("Start date must be prior to end date")

    dates = []
    cur_date = start_date
    while cur_date <= end_date:
        if cur_date.weekday() in range(5):  # Mon - Fri
            cur_date_str = cur_date.strftime("%Y%m%d")
            dates.append(cur_date_str)
        cur_date += datetime.timedelta(days=1)

    return dates


def HHmmss_to_sectime(HHmmss):
    if HHmmss is None:
        return None
    dt = datetime.datetime.strptime(HHmmss, "%H:%M:%S")
    return dt.hour * 60 * 60 + dt.minute * 60 + dt.second


def sectime_to_HHmmss(sectime):
    if sectime is None:
        return None
    hour = sectime / 3600
    minute = (sectime % 3600) / 60
    second = sectime % 60
    dt = datetime.datetime(2019, 1, 1, hour, minute, second)
    return dt.strftime("%H:%M:%S")


def sectime_diff(st1, st2):
    if st1 is None or st2 is None:
        return None
    diff = abs(st1 - st2)
    hour = diff / 3600
    minute = (diff % 3600) / 60
    second = diff % 60
    result = ''
    if st1 == st2:
        return '持平'
    elif st1 < st2:
        result += '早'
    else:
        result += '晚'

    if hour > 0:
        result += (str(hour) + '小时' + str(minute) + '分' + str(second) + '秒')
        return result

    if minute > 0:
        result += (str(minute) + '分' + str(second) + '秒')
        return result

    if second > 0:
        result += (str(second) + '秒')
        return result


def get_avg_sectime_table(person_times_table):
    person_avg_sectime_table = {}
    for item in person_times_table.items():
        sectimes = map(HHmmss_to_sectime, item[1])
        if len(sectimes) == 0:
            avg_sectime = None
        else:
            avg_sectime = sum(sectimes) / len(sectimes)
        person_avg_sectime_table[item[0]] = avg_sectime

    return person_avg_sectime_table


def get_stat_desc(person_avg_sectime_table):
    all_None = True
    max_avg_sectime = 0
    min_avg_sectime = 24 * 60 * 60
    max_avg_sectime_person = None
    min_avg_sectime_person = None
    sum = 0
    cnt = 0
    for item in person_avg_sectime_table.items():
        if item[1] is not None:
            all_None = False
            sum += item[1]
            cnt += 1
            if item[1] > max_avg_sectime:
                max_avg_sectime = item[1]
                max_avg_sectime_person = item[0]
            if item[1] < min_avg_sectime:
                min_avg_sectime = item[1]
                min_avg_sectime_person = item[0]
    if all_None:
        desc = dict(total_avg_sectime=None,
                    max_avg_sectime=None,
                    max_avg_sectime_person=None,
                    min_avg_sectime=None,
                    min_avg_sectime_person=None
                    )
    else:
        total_avg_sectime = sum / cnt
        desc = dict(total_avg_sectime=total_avg_sectime,
                    max_avg_sectime=max_avg_sectime,
                    max_avg_sectime_person=max_avg_sectime_person,
                    min_avg_sectime=min_avg_sectime,
                    min_avg_sectime_person=min_avg_sectime_person
                    )
    return desc


def get_trend(avg_send_times):
    from algorithms import linear_regression
    k = linear_regression(avg_send_times)
    if k > 0:
        return '下降趋势'
    elif k < 0:
        return '上升趋势'
    else:
        return '稳定趋势'


def person_stat(request):
    """
    request body:
    {
        "name": "胡明昊",
        "start_day": "20190701",
        "end_day": "20190723"
    }

    if end_day isn't given, default to today
    if start_day isn't given, default to show last month (30 days)

    response:
    {
        "date": ["20191211", "20191212", "20191213"],
        "time": [null, "11:02:09", "13:05:59"],
        "total_avg": "11:30:22",
        "your_avg": "11:19:31",
        "you_diff": "早11分",
        "beyond_percentage": "84%"
    }
    """
    if request.method == 'POST':
        dct = json.loads(request.body)
        name = dct['name']
        start_date_str = dct.get('start_date')
        end_date_str = dct.get('end_date')

        if name not in staffs:
            raise ValueError("Name not in staff list")

        dates = check_date(start_date_str, end_date_str)
        msg_times = []
        person_times_table = {}
        for person in staffs:
            person_times_table[person] = []
        for date in dates:
            msg_time = None
            record_path = os.path.join(root_dir, "data/records/%s.json" % date)
            if os.path.exists(record_path):
                with codecs.open(record_path) as f:
                    record = json.load(f)
                chenbao_list = record['chenbao_list']
                for chenbao in chenbao_list:
                    if chenbao['name'] not in staffs:
                        continue  # staff no longer here
                    person_times_table[chenbao['name']].append(chenbao['time'])
                    if chenbao['name'] == name:
                        msg_time = chenbao['time']
            msg_times.append(msg_time)

        person_avg_sectime_table = get_avg_sectime_table(person_times_table)
        desc = get_stat_desc(person_avg_sectime_table)
        your_avg_sectime = person_avg_sectime_table[name]
        if your_avg_sectime is not None:
            sorted_person_avg_sectimes = sorted(filter(lambda x: x is not None, person_avg_sectime_table.values()),
                                                reverse=True)
            person_after_you_num = sorted_person_avg_sectimes.index(your_avg_sectime)
            beyond_percentage = "%d%%" % int((float(person_after_you_num) / len(sorted_person_avg_sectimes)) * 100)
        else:
            beyond_percentage = None

        response_dict = dict(date=dates,
                             time=msg_times,
                             total_avg=sectime_to_HHmmss(desc['total_avg_sectime']),
                             your_avg=sectime_to_HHmmss(your_avg_sectime),
                             you_diff=sectime_diff(your_avg_sectime, desc['total_avg_sectime']),
                             beyond_percentage=beyond_percentage)

        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def person_history(request):
    """
    request body:
    {
        "name": "胡明昊",
        "start_day": "20190701",
        "end_day": "20190723"
    }

    if end_day isn't given, default to today
    if start_day isn't given, default to show last month (30 days)

    response:
    {
        "date": ["20191211", "20191212", "20191213"],
        "content": ["xxx", "xxx", "xxxx"]
    }
    """
    if request.method == 'POST':
        dct = json.loads(request.body)
        name = dct['name']
        start_date_str = dct.get('start_date')
        end_date_str = dct.get('end_date')

        if name not in staffs:
            raise ValueError("Name not in staff list")

        dates = check_date(start_date_str, end_date_str)
        contents = []
        for date in dates:
            content = None
            record_path = os.path.join(root_dir, "data/records/%s.json" % date)
            if os.path.exists(record_path):
                with codecs.open(record_path) as f:
                    record = json.load(f)
                chenbao_list = record['chenbao_list']
                for chenbao in chenbao_list:
                    if chenbao['name'] not in staffs:
                        continue  # staff no longer here
                    if chenbao['name'] == name:
                        content = chenbao['content']
                        break
            contents.append(content)

        response_dict = dict(date=dates, content=contents)
        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def total_stat(request):
    """
    request body:
    {
        "start_day": "20190701",
        "end_day": "20190723"
    }

    if end_day isn't given, default to today
    if start_day isn't given, default to show last month (30 days)

    response:
    {
        "date": ["20191211", "20191212", "20191213"],
        "total_staff": [30, 31, 31],
        "absent_person": [1, 2, 2],
        "sent_cb_person": [26, 28, 27],
        "avg_send_time": ["11:18:21", "12:32:45", "15:23:23"],
        "total_avg": "13:23:56",
        "trend": "上升趋势",
        "earliest_person": "胡明昊",
        "earliest_diff": "早1小时12分",
        "latest_person": "黎吾平",
        "latest_diff": "晚2小时42分",
    }
    """
    if request.method == 'POST':
        dct = json.loads(request.body)
        response_dict = total_stat_helper(dct)
        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def total_stat_helper(dct):
    start_date_str = dct.get('start_date')
    end_date_str = dct.get('end_date')

    dates = check_date(start_date_str, end_date_str)
    total_staffs = []
    absent_persons = []
    sent_cb_persons = []
    avg_send_times = []
    avg_send_sectimes = []
    person_times_table = {}
    for person in staffs:
        person_times_table[person] = []
    for date in dates:
        record_path = os.path.join(root_dir, "data/records/%s.json" % date)
        if os.path.exists(record_path):
            with codecs.open(record_path) as f:
                record = json.load(f)
            total_staffs.append(record['total_staff'])
            absent_persons.append(record['absent'])
            sent_cb_persons.append(len(record['chenbao_list']))
            chenbao_list = record['chenbao_list']
            tmp = map(lambda x: HHmmss_to_sectime(x['time']), chenbao_list)
            tmp_avg_send_sectime = sum(tmp) / len(tmp)
            avg_send_sectimes.append(tmp_avg_send_sectime)
            avg_send_times.append(sectime_to_HHmmss(tmp_avg_send_sectime))
            for chenbao in chenbao_list:
                if chenbao['name'] not in staffs:
                    continue  # staff no longer here
                person_times_table[chenbao['name']].append(chenbao['time'])

        else:
            total_staffs.append(None)
            absent_persons.append(None)
            sent_cb_persons.append(None)
            avg_send_times.append(None)

    person_avg_sectime_table = get_avg_sectime_table(person_times_table)
    desc = get_stat_desc(person_avg_sectime_table)

    response_dict = dict(date=dates,
                         total_staff=total_staffs,
                         absent_person=absent_persons,
                         sent_cb_person=sent_cb_persons,
                         avg_send_time=avg_send_times,
                         total_avg=sectime_to_HHmmss(desc['total_avg_sectime']),
                         trend=get_trend(avg_send_sectimes),
                         earliest_person=desc["min_avg_sectime_person"],
                         earliest_diff=sectime_diff(desc["min_avg_sectime"], desc['total_avg_sectime']),
                         latest_person=desc["max_avg_sectime_person"],
                         latest_diff=sectime_diff(desc["max_avg_sectime"], desc['total_avg_sectime']))
    return response_dict


def stat_rank(dct):
    """
    START: copy the first part of total_stat_helper for temporary use
    """
    start_date_str = dct.get('start_date')
    end_date_str = dct.get('end_date')

    dates = check_date(start_date_str, end_date_str)
    total_staffs = []
    absent_persons = []
    sent_cb_persons = []
    avg_send_times = []
    avg_send_sectimes = []
    person_times_table = {}
    for person in staffs:
        person_times_table[person] = []
    for date in dates:
        record_path = os.path.join(root_dir, "data/records/%s.json" % date)
        if os.path.exists(record_path):
            with codecs.open(record_path) as f:
                record = json.load(f)
            total_staffs.append(record['total_staff'])
            absent_persons.append(record['absent'])
            sent_cb_persons.append(len(record['chenbao_list']))
            chenbao_list = record['chenbao_list']
            tmp = map(lambda x: HHmmss_to_sectime(x['time']), chenbao_list)
            tmp_avg_send_sectime = sum(tmp) / len(tmp)
            avg_send_sectimes.append(tmp_avg_send_sectime)
            avg_send_times.append(sectime_to_HHmmss(tmp_avg_send_sectime))
            for chenbao in chenbao_list:
                if chenbao['name'] not in staffs:
                    continue  # staff no longer here
                person_times_table[chenbao['name']].append(chenbao['time'])

        else:
            total_staffs.append(None)
            absent_persons.append(None)
            sent_cb_persons.append(None)
            avg_send_times.append(None)

    person_avg_sectime_table = get_avg_sectime_table(person_times_table)
    """
    END: copy the first part of total_stat_helper for temporary use
    """
    rank = sorted(person_avg_sectime_table.items(), key=lambda x: x[1])
    top_ten_sectime = rank[:10]
    top_ten = [(x[0], sectime_to_HHmmss(x[1])) for x in top_ten_sectime]
    return top_ten


def chat_recognizer(request):
    if request.method == 'GET':
        from chenbao.features.chat_recognizer.model import ChatRecognizer
        cr = ChatRecognizer()
        cr.load()
        doc = request.GET.get('chat')
        logger.debug(doc)
        labels, probs = cr.test_one(doc)
        meaningful_label = ['否', '是']
        print_label = meaningful_label[labels[0]]
        print_prob = probs[0]
        result = "Predict: %s (%.2f%%)  --- 「%s」" % (print_label, print_prob * 100, doc)

        return HttpResponse(result, content_type="text/html", charset='utf-8')


def test_distribution(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        return HttpResponse('This is %s' % id, content_type="text/html")


def test_django(request):
    if request.method == 'POST':
        return HttpResponse(json.dumps({'rc': 0}), content_type="application/json")


def run(request, **kwargs):
    return render(request, 'index.html')
