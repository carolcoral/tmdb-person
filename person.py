#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import xml.etree.ElementTree as ET
import json


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
    def __init__(self, tmdb_id, actor_path, tmdb_token):
        self.image_path = None
        self.tmdb_id = tmdb_id
        self.actor_path = actor_path
        self.tmdb_token = tmdb_token

    def get_actor_info(self):
        url = "https://api.themoviedb.org/3/person/" + self.tmdb_id + "?language=zh-CN"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.tmdb_token
        }
        response = requests.get(url, headers=headers)
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


def __execute(dir_path, output, tmdb_token):
    __file_paths = []
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
        print("开始处理元数据刮削识别:{0}".format(__file_path))
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
            if ".nfo" not in os.listdir(__path_dir):
                __actor_info = Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token).get_actor_info()
                print(__actor_info)
            if "folder" not in os.listdir(__path_dir):
                Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir, tmdb_token=tmdb_token).get_actor_image()


if __name__ == '__main__':
    # 扫描目录
    __dir_path = "example/movies"
    # 输出演员元数据目录
    __output = "data/metadata/person"
    # TMDB API TOKEN
    __tmdb_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTU4ODAxMGY5OTUwYWEyNThhYjFhYjJlMjI4NGVmYSIsInN1YiI6IjYxYmRmOGNjMzgzZGYyMDA0MjIzNDhjOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RPG8F8AELlK7MgrXDR2U0YRv61VteZZ9ponilnkQqkE"
    # 开始执行主程序
    __execute(dir_path=__dir_path, output=__output, tmdb_token=__tmdb_token)
