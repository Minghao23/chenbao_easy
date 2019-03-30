# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import re
import codecs

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

        import datetime
        to = "rd@yottabyte.cn; presale@yottabyte.cn; postsale@yottabyte.cn;"
        cc = "chen.jun@yottabyte.cn;"
        subject = "北京晨会-%s" % datetime.datetime.now().strftime("%Y%m%d")
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
    cbs = map(lambda x: x[1:] if len(x) > 0 and x[0] == '\n' else x, cbs)  # remove \n suffix and prefix
    cbs = map(lambda x: x[:-1] if len(x) > 0 and x[-1] == '\n' else x, cbs)

    chenbao_list = []
    for cb in cbs:
        if len(cb) >= 2 and cb[:2] in staffs:
            name = cb[:2]
        elif len(cb) >= 3 and cb[:3] in staffs:
            name = cb[:3]
        else:
            continue

        content = re.sub(re.compile(r'.*\n'), '', cb, 1)
        chenbao_list.append({'name': name, 'content': content})

    return chenbao_list
