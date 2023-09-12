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

from tmdb import Tmdb


def __redo(log, output, tmdb_token, language="zh-CN"):
    with open("./error_tmdb_ids.txt", "r") as error_f:
        error_info = error_f.read()
        for info in error_info.split(","):
            info = info.strip()
            __tmdbid = info.split("-")[2]
            __actor_name = info.split("-")[0]
            __name = __actor_name[0].lower()
            __full_actor_name = __actor_name + "-tmdb-" + __tmdbid
            __path_dir = os.path.join(output, __name, __full_actor_name)
            if not os.path.exists(__path_dir):
                os.makedirs(__path_dir)
            # 如果存在元数据则不再进行刮削
            if "person.nfo" not in os.listdir(__path_dir):
                Tmdb(log=log, tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token,
                     language=language).create_actor_nfo()
            else:
                log.logger.info("当前路径已存在person.nfo文件, 跳过刮削:{0}".format(__path_dir))
            # 如果存在海报则不再进行刮削
            if "folder.jpg" not in os.listdir(__path_dir):
                Tmdb(log=log, tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token,
                     language=language).get_actor_image()
            else:
                log.logger.info("当前路径已存在folder.jpg文件, 跳过刮削:{0}".format(__path_dir))


if __name__ == '__main__':
    os.remove("./error_tmdb_ids.txt")
    error_file = open("./error_tmdb_ids.txt", "w+")
    for i in os.listdir("data/data/metadata/error"):
        print(i)
        error_file.write(i+",")
    error_file.close()
