# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import re
import codecs
import os
import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

with codecs.open('data/staffs.json') as f:
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

        to = "rd@yottabyte.cn; presale@yottabyte.cn; postsale@yottabyte.cn;"
        cc = "chen.jun@yottabyte.cn;"
        subject = "北京晨会-%s" % today_str
        message = '\n\n'.join(['[%s]\n%s' % (chenbao['name'], chenbao['content']) for chenbao in chenbao_list])
        message = '\n发报人数：%d\n请假人员：%s\n\n\n%s' % (len(chenbao_list), ' '.join(absent_persons), message)

        response_dict = {'to': to, 'cc': cc, 'subject': subject, 'message': message}
        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def get_chenbao_list(chat_content):
    pattern_header = re.compile(ur'\S*\s{2}\d{2}:\d{2}:\d{2}\n')
    pattern_recall = re.compile(ur'.*撤回了一条消息.*\n')
    pattern_change = re.compile(ur'.*((加入群)|(退出群)|(移出群))\n')

    with codecs.open('data/staffs.json') as f:
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
    dt = datetime.datetime.strptime(HHmmss, "%H:%M:%S")
    return dt.hour * 60 * 60 + dt.minute * 60 + dt.second


def sectime_to_HHmmss(sectime):
    hour = sectime / 3600
    minute = (sectime % 3600) / 60
    second = sectime % 60
    dt = datetime.datetime(2019, 1, 1, hour, minute, second)
    return dt.strftime("%H:%M:%S")


def sectime_diff(st1, st2):
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
        "total_average": "11:30:22",
        "you_diff": "早1小时20分",
        "earliest_person": "胡明昊",
        "earliest_diff": "早2小时18分",
        "latest_person": "黎吾平",
        "latest_diff": "晚1小时28分",
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
                    person_times_table[chenbao['name']].append(chenbao['time'])
                    if chenbao['name'] == name:
                        msg_time = chenbao['time']
            msg_times.append(msg_time)

        person_avg_sectime_table = {}
        for item in person_times_table.items():
            sectimes = map(HHmmss_to_sectime, item[1])
            if len(sectimes) == 0:
                avg_sectime = 0
            else:
                avg_sectime = sum(sectimes) / len(sectimes)
            person_avg_sectime_table[item[0]] = avg_sectime

        valid_person_avg_sectime = filter(lambda x: x > 0, person_avg_sectime_table.values())
        if len(valid_person_avg_sectime) == 0:
            total_average_sectime = 0
        else:
            total_average_sectime = sum(valid_person_avg_sectime) / len(valid_person_avg_sectime)
        earliest_person = min(person_avg_sectime_table, key=person_avg_sectime_table.get)
        earliest_diff = sectime_diff(person_avg_sectime_table[earliest_person], total_average_sectime)
        latest_person = max(person_avg_sectime_table, key=person_avg_sectime_table.get)
        latest_diff = sectime_diff(person_avg_sectime_table[latest_person], total_average_sectime)
        you_diff = sectime_diff(person_avg_sectime_table[name], total_average_sectime)
        total_average = sectime_to_HHmmss(total_average_sectime)

        response_dict = dict(date=dates, time=msg_times, total_average=total_average, you_diff=you_diff,
                             earliest_person=earliest_person, earliest_diff=earliest_diff,
                             latest_person=latest_person, latest_diff=latest_diff)
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
    }
    """
    if request.method == 'POST':
        dct = json.loads(request.body)
        start_date_str = dct.get('start_date')
        end_date_str = dct.get('end_date')

        dates = check_date(start_date_str, end_date_str)
        total_staffs = []
        absent_persons = []
        sent_cb_persons = []
        for date in dates:
            record_path = os.path.join(root_dir, "data/records/%s.json" % date)
            if os.path.exists(record_path):
                with codecs.open(record_path) as f:
                    record = json.load(f)
                total_staffs.append(record['total_staff'])
                absent_persons.append(record['absent'])
                sent_cb_persons.append(len(record['chenbao_list']))
            else:
                total_staffs.append(None)
                absent_persons.append(None)
                sent_cb_persons.append(None)

        response_dict = dict(date=dates, total_staff=total_staffs,
                             absent_person=absent_persons, sent_cb_person=sent_cb_persons)
        response_json = json.dumps(response_dict)

        return HttpResponse(response_json, content_type="application/json")


def run(request, **kwargs):
    return render(request, 'index.html')
