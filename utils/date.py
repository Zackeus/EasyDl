#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : date.py 
# @Software: PyCharm
# @Time : 2019/4/3 10:54


import datetime
import time

_TIME_FORMAT = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']


def in_time_zones(start_time, end_time, check_time=time.time()):
    """
    判断时间是否在指定时间段内
    :param check_time: 待判断时间
    :param start_time: 起始时间
    :param end_time: 结束时间
    :return:
    """
    if isinstance(start_time, datetime.datetime):
        start_time = int(time.mktime(start_time.timetuple()))
    if isinstance(end_time, datetime.datetime):
        end_time = int(time.mktime(end_time.timetuple()))
    if isinstance(check_time, datetime.datetime):
        check_time = int(time.mktime(check_time.timetuple()))
    return True if start_time <= check_time <= end_time else False


def get_before_dawn(time_stamp=datetime.date.today()):
    """
    获取某天的开始时间戳(凌晨零点)
    :param time_stamp:时间戳
    :return:
    """
    if isinstance(time_stamp, float):
        time_stamp = datetime.datetime.fromtimestamp(time_stamp)
    return int(time.mktime(time.strptime(str(time_stamp.strftime('%Y-%m-%d')), '%Y-%m-%d')))


def get_end_dawn(time_stamp=datetime.date.today()):
    """
    获取某天的结束时间戳
    :param time_stamp:
    :return:
    """
    if isinstance(time_stamp, float):
        time_stamp = datetime.datetime.fromtimestamp(time_stamp)
    tomorrow = time_stamp + datetime.timedelta(days=1)
    return int(time.mktime(time.strptime(str(tomorrow.strftime('%Y-%m-%d')), '%Y-%m-%d'))) - 1


def str_to_time(s, format=_TIME_FORMAT[0]):
    """
    时间字符转时间
    :param s:
    :param format:
    :return:
    """
    return datetime.datetime.strptime(s, format)


def s_to_time(s):
    """
    将秒转为时间格式
    :param long s:
    :return:
    """
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return '%d:%02d:%02d' % (h, m, s)


def ms_to_time(ms):
    """
    将毫秒转为时间格式
    :param long ms:
    :return:
    """
    s, ms = divmod(ms, 1000)
    return s_to_time(s)


if __name__ == '__main__':
    # start_time = get_before_dawn(time.time())
    # print(datetime.datetime.fromtimestamp(start_time))
    # end_time = get_end_dawn(time.time())
    # print(datetime.datetime.fromtimestamp(end_time))
    #
    # tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    # print(in_time_zones(start_time, end_time, tomorrow))

    print(ms_to_time(13270))