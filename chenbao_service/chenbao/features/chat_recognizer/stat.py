# encoding=utf-8
import pandas as pd
from collections import Counter


def rank():
    df_result = pd.read_csv('data/dataset_verified.csv').astype('str')  # must add astype('str) to avoid codec problem
    df = pd.read_csv('data/qq_record_190123-191209.csv').astype('str')  # must add astype('str) to avoid codec problem
    df['label'] = df_result['label']
    df = df[df['label'] == '1']
    names = df['name'].values.tolist()
    cnt = Counter(names)
    print "=== 2019年度日志易迟到早退排行榜 ==="
    for i, item in enumerate(cnt.most_common()):
        rank_num = "No.%d" % (i + 1)
        name = item[0]
        times = "%d次" % item[1]

        placeholder_rank_num = 5

        print "%s%s - %s（%s）" % (rank_num, (placeholder_rank_num - len(rank_num)) * " ", name, times)


rank()
