# -*- coding: utf-8 -*-
import re
import codecs
import json
import numpy as np
import pandas as pd

raw_file = 'data/qq_record_raw_190123-191209.txt'
csv_file = 'data/qq_record_190123-191209.csv'


def raw_to_csv():
    with codecs.open(raw_file, 'r', 'utf-8') as f:
        raw_corpus = f.read()

    pattern_header = re.compile(ur'\S*\s{2}\d{2}:\d{2}:\d{2}\n')
    pattern_recall = re.compile(ur'.*((撤回了一条消息)|(recalled a message)).*\n')
    pattern_change = re.compile(ur'.*((加入群)|(退出群)|(移出群))\n')

    with codecs.open('data/staffs.json') as f:
        staffs = json.load(f)["staffs"]

    out = re.sub(pattern_recall, "", raw_corpus)
    out = re.sub(pattern_change, "", out)
    contents = re.split(pattern_header, out)
    contents = contents[1:]  # drop the first meaningless string
    contents = map(lambda x: x[1:] if len(x) > 0 and x[0] == '\n' else x, contents)  # remove \n suffix and prefix
    contents = map(lambda x: x[:-1] if len(x) > 0 and x[-1] == '\n' else x, contents)
    headers = re.findall(pattern_header, out)
    times = map(lambda x: x[-9: -1], headers)
    names = map(lambda x: x[: -11], headers)

    # check if is a chenbao
    is_chenbao = []
    for i, content in enumerate(contents):
        content = content.strip()
        # content = content.strip(u'\u0010')
        if len(content) >= 2 and content[:2] in staffs:
            is_chenbao.append(1)
        elif len(content) >= 3 and content[:3] in staffs:
            is_chenbao.append(1)
        elif content[:9] == 'Catherine' or content[:9] == 'catherine':
            is_chenbao.append(1)
        else:
            is_chenbao.append(0)

    date = [None for _ in range(len(names))]
    df = pd.DataFrame({'name': names, 'date': date, 'time': times, 'content': contents, 'is_chenbao': is_chenbao},
                      columns=['name', 'date', 'time', 'content', 'is_chenbao'])
    df.to_csv(csv_file, index=False, encoding='utf-8')


def generate_train_dataset():
    content = pd.read_csv(csv_file).astype('str')['content']
    n = len(content)
    label = np.zeros(n, dtype='int')
    for i in range(n):
        if re.match(r'.*(晚|早|会|走|先|事).*', content[i]) is not None:
            label[i] = 1

    df = pd.DataFrame({'value': content, 'label': label}, columns=['value', 'label'])
    df.to_csv('data/dataset.csv', index=False, encoding='utf-8')


# raw_to_csv()
generate_train_dataset()

# print re.match(r'.*会.*', '有点头疼，今天早走一会。')
