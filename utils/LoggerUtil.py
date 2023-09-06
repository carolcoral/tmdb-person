#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2019/4/15
    @Author  : LXW
    @Site    : 
    @File    : LoggerUtil.py
    @Software: PyCharm
    @Description: 日志工具，默认保存文件在当前文件夹下
"""
import logging
from logging import handlers
from functools import wraps
import traceback
import os


class Logger(object):
    """
    日志封装类：
     1. 作用是同时打印和写日志文件。
     2. 业务日志如果是需要告警或者邮件，则走warning。
     3. 运行出错则走error
     4. record用来切片函数，记录函数开始和结束。
    """
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

    def record(self, arg):
        def _log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.info(arg + '_开始----' + func.__name__)
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    desc = "%s_traceback.format_exc(): %s" % (e, traceback.format_exc())
                    self.logger.error(desc)
                    self.logger.info(arg + '_中断----' + func.__name__)
                    # exit(1)
                    return False
                else:
                    self.logger.info(arg + '_结束----' + func.__name__)
                return ret

            return wrapper

        return _log
