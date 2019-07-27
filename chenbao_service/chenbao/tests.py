# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import datetime

# Create your tests here.

def check_date(start_date_str, end_date_str):
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
        cur_date_str = cur_date.strftime("%Y%m%d")
        dates.append(cur_date_str)
        cur_date += datetime.timedelta(days=1)

    return dates


# check_day(None, "20120123")
# check_day(None, "20120223")
# check_day(None, "20120323")
# check_day(None, "20120423")
# check_day(None, "20120523")
# check_day(None, "20120623")
# check_day(None, "20120723")
# check_day(None, "20120823")
# check_day(None, "20120923")
# check_day(None, "20121023")
# check_day(None, "20121123")
# check_day(None, "20121223")
#
# check_day("20121224", "20121223")
print check_date("20120422", "20120423")
