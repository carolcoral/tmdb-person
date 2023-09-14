#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 多线程模式执行脚本
import os
import shutil

from main import __init_logger, __get_sys_args, __check_version, __create_default_dirs
from utils.scrape import Scrape


def __cut_dirs(log, dir_path, output):
    log.logger.info("开始执行元数据文件分组:{0}".format(dir_path))
    # 默认 language="zh-CN" (简体中文),可以通过修改 "language" 的值变更获取元数据的语言类别
    # 将nfo文件根据首字母小些切分成不同的文件夹
    nfo_list = os.path.join(os.path.dirname(output), "nfo_list")
    if not os.path.exists(nfo_list):
        os.makedirs(nfo_list)
    for nfo_file_dir in dir_path:
        for nfo_file in os.listdir(nfo_file_dir):
            __name = nfo_file[0].lower()
            __path_dir = os.path.join(nfo_list, __name)
            if not os.path.exists(__path_dir):
                os.makedirs(__path_dir)
            shutil.copyfile(os.path.join(nfo_file_dir, nfo_file), os.path.join(__path_dir, nfo_file))
    log.logger.info("结束执行元数据文件分组:{0}".format(nfo_list))
    return nfo_list


if __name__ == '__main__':
    # 初始化日志
    __log = __init_logger()
    sys_args = __get_sys_args(log=__log)
    # 扫描目录
    __dir_path = ["data/metadata/nfo"]
    # 输出演员元数据目录
    __output = "data/metadata/person"
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
        __language = sys_args["__language"]
    # 检查python版本
    __check_version(log=__log)
    # 开始执行主程序
    __create_default_dirs()
    __nfo_list = __cut_dirs(log=__log, dir_path=__dir_path, output=__output)
    # 删除异常信息存储文件
    error_file_path = "./error_tmdb_ids.txt"
    if os.path.exists(error_file_path):
        os.remove(error_file_path)
    for dir_name in os.listdir(__nfo_list):
        scrape = Scrape(log=__log, dir_path=os.path.join(__nfo_list, dir_name), output=__output,
                        tmdb_token=__tmdb_token, language=__language)
        scrape.start()
