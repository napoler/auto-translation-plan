#!/usr/bin/env python
#!-*-coding:utf-8 -*-

import random
import datetime

def random_date(start='', end=''):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def yield_random_date(start='', end=''):
    """Generate a random datetime between `start` and `end`"""
    delta = int((end - start).total_seconds())
    while True:
        yield start + datetime.timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, delta),
        )
# end_time=datetime.datetime.now()
# start_time=datetime.datetime.now() + datetime.timedelta(minutes=-3) # 当前时间减去3分钟


import  hashlib
def md5(string):
    # 对要加密的字符串进行指定编码
    string = string.encode(encoding ='UTF-8')
    # md5加密
    # print(hashlib.md5(string))
    # 将md5 加密结果转字符串显示
    string = hashlib.md5(string).hexdigest()
    return string