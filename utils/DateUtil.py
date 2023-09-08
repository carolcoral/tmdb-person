# -*-encoding:utf-8 -*-

import datetime
import time

DEFAULT_DATE_FORMAT = '%Y-%m-%d'
FULL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_someday_before(n, fmt=DEFAULT_DATE_FORMAT):
    """获取n天前日期，返回的fmt日期格式"""
    yes = datetime.date.today() - datetime.timedelta(days=n)
    return yes.strftime(fmt)


def get_today(fmt=DEFAULT_DATE_FORMAT):
    """获取今天前日期，返回的fmt日期格式"""
    return get_someday_before(0, fmt)


def get_yesterday(fmt=DEFAULT_DATE_FORMAT):
    """获取昨天前日期，返回的fmt日期格式"""
    return get_someday_before(1, fmt)


def get_someday_before_tmp(n, ms=False):
    """获取n天前的时间戳"""
    yes = datetime.date.today() - datetime.timedelta(days=n)
    if ms:
        return time.mktime(yes.timetuple()) * 1000
    else:
        return time.mktime(yes.timetuple())


def get_today_tmp(ms=False):
    """获取今天前的时间戳"""
    return get_someday_before_tmp(0, ms)


def get_yesterday_tmp(n, ms=False):
    """获取昨天前的时间戳"""
    return get_someday_before_tmp(1, ms)


def get_now(fmt=DEFAULT_DATE_FORMAT):
    return datetime.datetime.now().strftime(fmt)
