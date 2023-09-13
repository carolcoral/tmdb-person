#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from analyze import Analyze
from tmdb import Tmdb


def __execute(log, dir_path, output, tmdb_token, language="zh-CN"):
    log.logger.info("------------------- 开始获取演员元数据及海报 -------------------")
    __file_paths = []
    log.logger.info("当前执行元数据刮削识别的根文件夹:{0}".format(dir_path))
    for folder in os.listdir(dir_path):
        __folder2 = os.path.join(dir_path, folder)
        # 判断是否文件夹
        if os.path.isdir(__folder2):
            for nfo_file in os.listdir(__folder2):
                __child_file_path = os.path.join(__folder2, nfo_file)
                if ".nfo" in os.path.basename(__child_file_path):
                    __file_paths.append(__child_file_path)
        elif os.path.isfile(__folder2):
            __file_name = os.path.basename(__folder2)
            if ".nfo" in __file_name:
                __file_paths.append(__folder2)
    for __file_path in __file_paths:
        log.logger.info("开始处理元数据刮削识别:{0}".format(__file_path))
        # __file_path = "example/神出鬼没 (2023) - 2160p.nfo"
        __nfo_data = Analyze(file_path=__file_path).analyze()
        for __actor in __nfo_data["actors"]:
            log.logger.info("当前解析的演员信息: {0}".format(__actor))
            if "tmdbid" in __actor.keys():
                __tmdbid = __actor["tmdbid"]
                __actor_name = __actor["name"]
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
    log.logger.info("------------------- 结束获取演员元数据及海报 -------------------")
