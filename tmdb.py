#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os


class Tmdb:
    def __init__(self, log, tmdb_id, actor_path, tmdb_token, language="zh-CN"):
        self.log = log
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
        self.log.logger.info("当前刮削到的演员元数据:{0}".format(response.text))
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
