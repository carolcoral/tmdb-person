#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from utils.collect_metadata import __collect_nfo
from utils.redo import __redo, __check
from utils.scrape import Scrape
from utils.LoggerUtil import Logger


def __init_logger(log_file="tmdb.log", level="info", back_count=3):
    """
    服务日志记录对象
    :param log_file: 日志文件名
    :param level: 日志记录级别。debug info warning error crit
    :param back_count: 日志文件备份天数
    :return: 日志对象
    """
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # (必填)日志文件名  log_file="/data/ws_env/logtest/process.log"
    log_file_abspath = os.path.join(father_path, "logs", log_file)
    return Logger(log_file_abspath, level=level, backCount=back_count)


def __check_version(log):
    version_info = sys.version_info
    if 3 > version_info.major:
        log.logger.error("当前Python版本不能小于3!")
        raise SystemExit(1)
    else:
        if 8 > version_info.minor:
            log.logger.error("当前Python版本不能小于3.8!")
            raise SystemExit(1)
        elif 8 == version_info.minor:
            log.logger.warn("推荐使用Python 3.9 及以上版本!")


def __get_sys_args(log):
    arg_json = {}
    size = len(sys.argv)
    if size == 1:
        return arg_json
    elif size > 1 and (size - 1) % 2 != 0:
        print(size)
        log.logger.error("请输入正确的配置参数!")
        raise SystemExit(1)
    i = 0
    arg_key = {}
    for arg in sys.argv:
        arg_key[arg] = i
        i = i + 1
    if "--dir_path" not in arg_key.keys():
        log.logger.error("请输入正确的扫描目录参数:{0}".format("--dir_path"))
        raise SystemExit(1)
    else:
        __dir_arg = sys.argv[arg_key["--dir_path"] + 1]
        dir_args = []
        for d_arg in __dir_arg.split(","):
            dir_args.append(d_arg.strip())
        arg_json["__dir_path"] = dir_args
    if "--output" not in arg_key.keys():
        log.logger.error("请输入正确的输出演员元数据目录参数:{0}".format("--output"))
        raise SystemExit(1)
    else:
        arg_json["__output"] = sys.argv[arg_key["--output"] + 1]
    if "--tmdb_token" not in arg_key.keys():
        log.logger.error("请输入正确的TMDB API TOKEN参数:{0}".format("--tmdb_token"))
        raise SystemExit(1)
    else:
        arg_json["__tmdb_token"] = sys.argv[arg_key["--tmdb_token"] + 1]
    if "--mode" not in arg_key.keys():
        log.logger.warn("未输入脚本执行模式，默认使用元数据文件转移模式:{0}".format("--mode"))
        arg_json["__mode"] = "collect"
    else:
        mode_value = sys.argv[arg_key["--mode"] + 1]
        if "collect" != mode_value and "scrape" != mode_value:
            log.logger.error("请输入正确的脚本执行模式:{0}".format(
                "collect(元数据文件转移)/scrape(元数据刮削)/redo(重新刮削异常元数据)"))
            raise SystemExit(1)
        arg_json["__mode"] = mode_value
    if "--language" not in arg_key.keys():
        log.logger.warn("未输入脚本执行语言，默认使用中文简体语言格式:{0}".format("--language"))
        arg_json["__language"] = "zh-CN"
    else:
        mode_value = sys.argv[arg_key["--language"] + 1]
        arg_json["__language"] = mode_value
    return arg_json


def __create_default_dirs():
    if not os.path.exists("./complete"):
        os.makedirs("./complete")
    if not os.path.exists("./redo"):
        os.makedirs("./redo")


def __master_execute(log, dir_path, output, tmdb_token, mode, language="zh-CN"):
    # 检查python版本
    __check_version(log=log)
    # 开始执行主程序
    __create_default_dirs()
    # 默认 language="zh-CN" (简体中文),可以通过修改 "language" 的值变更获取元数据的语言类别
    for __real_dir_path in dir_path:
        if "collect" == mode:
            __collect_nfo(log, __real_dir_path, output)
        if "scrape" == mode:
            # 删除异常信息存储文件
            error_file_path = "./error_tmdb_ids.txt"
            if os.path.exists(error_file_path):
                os.remove(error_file_path)
            scrape = Scrape(log=log, dir_path=__real_dir_path, output=output, tmdb_token=tmdb_token, language=language)
            scrape.start()
        if "redo" == mode:
            __redo(log=log, output=output, tmdb_token=tmdb_token, language=language)
        if "check" == mode:
            __check(scan_path=output)


if __name__ == '__main__':
    # 初始化日志
    __log = __init_logger()
    sys_args = __get_sys_args(log=__log)
    # 扫描目录
    __dir_path = ["/data/tmdb-person/data/metadata/nfo"]
    # 输出演员元数据目录
    __output = "/data/tmdb-person/data/metadata/person"
    # TMDB API TOKEN
    __tmdb_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTU4ODAxMGY5OTUwYWEyNThhYjFhYjJlMjI4NGVmYSIsInN1YiI6IjYxYmRmOGNjMzgzZGYyMDA0MjIzNDhjOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RPG8F8AELlK7MgrXDR2U0YRv61VteZZ9ponilnkQqkE"
    __mode = "scrape"
    __language = "zh-CN"
    if len(sys_args.keys()) > 0:
        # 扫描目录
        __dir_path = sys_args["__dir_path"]
        # 输出演员元数据目录
        __output = sys_args["__output"]
        # TMDB API TOKEN
        __tmdb_token = sys_args["__tmdb_token"]
        __mode = sys_args["__mode"]
        __language = sys_args["__language"]
    __master_execute(log=__log, dir_path=__dir_path, output=__output, tmdb_token=__tmdb_token, mode=__mode,
                     language=__language)
