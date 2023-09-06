#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import xml.etree.ElementTree as ET
import json
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


class Analyze:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        if "tvshow" in root.tag:
            data_json = {}
            self.__list_nodes(root, data_json)
            return data_json
        if "movie" in root.tag:
            data_json = {}
            self.__list_nodes(root, data_json)
            return data_json

    def __list_nodes(self, root, data):
        actors = []
        for node in root:
            if 0 == len(list(node)):
                data[node.tag] = node.text
            elif "actor" == node.tag:
                actor_json = {}
                self.__list_nodes(node, actor_json)
                actors.append(actor_json)
        data["actors"] = actors


class Tmdb:
    def __init__(self, tmdb_id, actor_path, tmdb_token, language="zh-CN"):
        self.image_path = None
        self.tmdb_id = tmdb_id
        self.actor_path = actor_path
        self.header = {
            "accept": "application/json",
            "Authorization": "Bearer " + tmdb_token
        }
        self.language = language

    def get_actor_info(self):
        url = "https://api.themoviedb.org/3/person/" + self.tmdb_id + "?language=" + self.language
        headers = self.header
        response = requests.get(url, headers=headers)
        log.logger.info("当前刮削到的演员元数据:{0}".format(response.text))
        return response.text

    def get_actor_image(self):
        image_path = json.loads(self.get_actor_info())["profile_path"]
        if None is not image_path:
            url = 'https://www.themoviedb.org/t/p/original' + image_path
            response = requests.get(url)
            if response.status_code == 200:
                suffix = image_path.split(".")[1]
                with open(os.path.join(self.actor_path, "folder." + suffix), 'wb') as f:
                    f.write(response.content)

    def __translations(self):
        url = "https://api.themoviedb.org/3/person/" + self.tmdb_id + "/translations"
        headers = self.header
        response = requests.get(url, headers=headers)
        return response.text

    def __get_actor_plot(self):
        translations = self.__translations()
        translations_list = json.loads(translations)["translations"]
        translations_json = {}
        for translation in translations_list:
            translations_json[translation["iso_3166_1"]] = translation
        plot = ""
        if "CN" in translations_json.keys():
            zh = translations_json["CN"]
            plot = zh["data"]["biography"]
        elif "US" in translations_json.keys():
            us = translations_json["US"]
            plot = us["data"]["biography"]
        return plot

    def create_actor_nfo(self):
        plot = self.__get_actor_plot()


def __execute(dir_path, output, tmdb_token):
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
            __tmdbid = __actor["tmdbid"]
            __actor_name = __actor["name"]
            __name = __actor_name[1].lower()
            __full_actor_name = __actor_name + "-tmdb-" + __tmdbid
            __path_dir = os.path.join(output, __name, __full_actor_name)
            if not os.path.exists(__path_dir):
                os.makedirs(__path_dir)
            # 如果存在元数据则不再进行刮削
            if "person.nfo" not in os.listdir(__path_dir):
                Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token).get_actor_info()
            # 如果存在海报则不再进行刮削
            if "folder.jpg" not in os.listdir(__path_dir):
                Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token).get_actor_image()


if __name__ == '__main__':
    # 扫描目录
    __dir_path = "example/movies"
    # 输出演员元数据目录
    __output = "data/metadata/person"
    # TMDB API TOKEN
    __tmdb_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTU4ODAxMGY5OTUwYWEyNThhYjFhYjJlMjI4NGVmYSIsInN1YiI6IjYxYmRmOGNjMzgzZGYyMDA0MjIzNDhjOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RPG8F8AELlK7MgrXDR2U0YRv61VteZZ9ponilnkQqkE"
    # 初始化日志
    log = __init_logger()
    # 开始执行主程序
    # 默认 language="zh-CN" (简体中文),可以通过修改 "language" 的值变更获取元数据的语言类别
    __execute(dir_path=__dir_path, output=__output, tmdb_token=__tmdb_token)
