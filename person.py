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
    def __init__(self, tmdb_id, actor_path):
        self.image_path = None
        self.tmdb_id = tmdb_id
        self.actor_path = actor_path

    def get_actor_info(self):
        url = "https://api.themoviedb.org/3/person/" + self.tmdb_id + "?language=zh-CN"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTU4ODAxMGY5OTUwYWEyNThhYjFhYjJlMjI4NGVmYSIsInN1YiI6IjYxYmRmOGNjMzgzZGYyMDA0MjIzNDhjOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RPG8F8AELlK7MgrXDR2U0YRv61VteZZ9ponilnkQqkE"
        }
        response = requests.get(url, headers=headers)
        return response.text

    def get_actor_image(self):
        image_path = json.loads(self.get_actor_info())["profile_path"]
        url = 'https://www.themoviedb.org/t/p/original' + image_path
        response = requests.get(url)
        if response.status_code == 200:
            suffix = image_path.split(".")[1]
            with open(os.path.join(self.actor_path, "folder." + suffix), 'wb') as f:
                f.write(response.content)


if __name__ == '__main__':
    __nfo_data = Analyze(file_path="example/神出鬼没 (2023) - 2160p.nfo").analyze()
    for __actor in __nfo_data["actors"]:
        __tmdbid = __actor["tmdbid"]
        __actor_name = __actor["name"]
        __name = __actor_name[1].lower()
        __path_dir = os.path.join("data", __name, __actor_name)
        if not os.path.exists(__path_dir):
            os.makedirs(__path_dir)
        if ".nfo" not in os.listdir(__path_dir):
            __actor_info = Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir).get_actor_info()
            print(__actor_info)
        if "folder" not in os.listdir(__path_dir):
            Tmdb(tmdb_id=__tmdbid, actor_path=__path_dir).get_actor_image()
