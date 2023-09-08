#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def __move(log, dir_file_path, output):
    with open(dir_file_path, "r") as read_f:
        file_name = os.path.basename(dir_file_path)
        if "tvshow" in file_name:
            file_name = os.path.basename(os.path.dirname(dir_file_path)) + ".nfo"
        output_file_path = os.path.join(output, file_name)
        with open(output_file_path, "w") as write_f:
            write_f.write(read_f.read())
    log.logger.info("当前完成文件转移:{0}".format(dir_file_path))


def __collect_nfo(log, dir_path, output):
    if not os.path.exists(output):
        os.makedirs(output)
    log.logger.info("------------------- 开始转移演员元数据NFO文件 -------------------")
    __file_paths = []
    log.logger.info("当前转移元数据刮削识别的根文件夹:{0}".format(dir_path))
    for folder in os.listdir(dir_path):
        __folder2 = os.path.join(dir_path, folder)
        # 判断是否文件夹
        if os.path.isdir(__folder2):
            for nfo_file in os.listdir(__folder2):
                __child_file_path = os.path.join(__folder2, nfo_file)
                if ".nfo" in os.path.basename(__child_file_path):
                    __move(log, __child_file_path, output)
        elif os.path.isfile(__folder2):
            __file_name = os.path.basename(__folder2)
            if ".nfo" in __file_name:
                __move(log, __folder2, output)
    log.logger.info("------------------- 结束转移演员元数据NFO文件 -------------------")
