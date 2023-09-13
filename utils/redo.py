#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2023/09/11
    @Author  : LXW
    @Site    : 
    @File    : redo.py
    @Software: PyCharm
    @Description:
    针对刮削出现异常的TMDB演员元数据进行重新补偿操作
"""
import os

from utils.tmdb import Tmdb


def __redo(log, output, tmdb_token, language="zh-CN"):
    redo_path = "../redo/error_tmdb_ids.txt"
    log.logger.info("------------------- 开始重新刮削: {0} -------------------".format(redo_path))

    with open(redo_path, "r") as error_f:
        error_info = error_f.read()
        for info in error_info.split(","):
            info = info.strip()
            if "" == info:
                break
            __tmdb_id = info.split("-tmdb-")[1]
            __actor_name = info.split("-tmdb-")[0]
            __name = __actor_name[0].lower()
            __full_actor_name = __actor_name + "-tmdb-" + __tmdb_id
            __path_dir = os.path.join(output, __name, __full_actor_name)
            if not os.path.exists(__path_dir):
                os.makedirs(__path_dir)
            # 如果存在元数据则覆盖刮削
            Tmdb(log=log, tmdb_id=__tmdb_id, actor_path=__path_dir, tmdb_token=tmdb_token,
                 language=language).create_actor_nfo(redo=True)
            # 如果存在海报则不再进行刮削
            if "folder.jpg" not in os.listdir(__path_dir):
                Tmdb(log=log, tmdb_id=__tmdb_id, actor_path=__path_dir, tmdb_token=tmdb_token,
                     language=language).get_actor_image()
            else:
                log.logger.info("当前路径已存在folder.jpg文件, 跳过刮削:{0}".format(__path_dir))
    log.logger.info("------------------- 结束重新刮削: {0} -------------------".format(redo_path))


def __check(scan_path="data/metadata/person"):
    no_nfo_tmdb_ids = "../redo/check/no_nfo_tmdb_ids.txt"
    no_image_tmdb_ids = "../redo/check/no_image_tmdb_ids.txt"
    if os.path.exists(no_nfo_tmdb_ids):
        os.remove(no_nfo_tmdb_ids)
    if os.path.exists(no_image_tmdb_ids):
        os.remove(no_image_tmdb_ids)
    error_file_nfo = open(no_nfo_tmdb_ids, "w+")
    error_file_image = open(no_image_tmdb_ids, "w+")
    for i in os.listdir(scan_path):
        for files in os.listdir(os.path.join(scan_path, i)):
            if "person.nfo" not in os.listdir(os.path.join(scan_path, i, files)):
                error_file_nfo.write(files + "\n")
            if "folder.jpg" not in os.listdir(os.path.join(scan_path, i, files)):
                error_file_image.write(files + "\n")
    error_file_nfo.close()
    error_file_image.close()
