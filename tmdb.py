#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
from analyze import Make
import utils.DateUtil as DateUtil

# https://api.tmdb.org
# https://tmdb.nastool.org
# https://t.nastool.workers.dev
# https://api.themoviedb.org
api_url = "https://api.tmdb.org"
image_url = "https://www.themoviedb.org"


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
        url = api_url + "/3/person/" + self.tmdb_id + "?language=" + self.language
        headers = self.header
        response = requests.get(url, headers=headers)
        return response.text

    def get_actor_image(self):
        image_path = json.loads(self.get_actor_info())["profile_path"]
        self.log.logger.info("当前刮削到的演员海报路径:{0}".format(image_path))
        if None is not image_path:
            url = image_url + '/t/p/original' + image_path
            response = requests.get(url)
            if response.status_code == 200:
                suffix = image_path.split(".")[1]
                with open(os.path.join(self.actor_path, "folder." + suffix), 'wb') as f:
                    f.write(response.content)

    def __translations(self):
        url = api_url + "/3/person/" + self.tmdb_id + "/translations"
        headers = self.header
        response = requests.get(url, headers=headers)
        return response.text

    def get_actor_plot(self):
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
        plot = plot.replace("\n", "").replace("\r\n", "")
        return plot

    def create_actor_nfo(self):
        actor_json = {}
        plot = self.get_actor_plot()
        actor_json["plot"] = plot
        actor_json["outline"] = plot
        actor_json["lockdata"] = "true"
        actor_json["lockedfields"] = "Name|SortName"
        actor_json["dateadded"] = DateUtil.get_now(DateUtil.FULL_DATE_FORMAT)

        actor_info = self.get_actor_info()
        self.log.logger.info("当前刮削到的演员元数据:{0}".format(actor_info))
        info_json = json.loads(actor_info)
        name = info_json["name"]
        actor_json["title"] = name
        birthday = info_json["birthday"]
        actor_json["premiered"] = birthday
        actor_json["releasedate"] = birthday

        year = "" if birthday is None else birthday.split("-")[0]

        actor_json["year"] = year
        actor_json["sorttitle"] = name
        actor_json["tmdbid"] = self.tmdb_id
        actor_json["language"] = "zh-CN"
        actor_json["countrycode"] = "CN"
        actor_json["placeofbirth"] = info_json["place_of_birth"]
        actor_json["uniqueid"] = self.tmdb_id

        actor_json["adult"] = "" if info_json["adult"] is None else str(info_json["adult"])
        actor_json["alsoknownas"] = "" if info_json["also_known_as"] is None else info_json["also_known_as"]
        actor_json["deathday"] = "" if info_json["deathday"] is None else str(info_json["deathday"])
        actor_json["gender"] = "" if info_json["gender"] is None else str(info_json["gender"])
        actor_json["homepage"] = "" if info_json["homepage"] is None else str(info_json["homepage"])
        actor_json["imdbid"] = "" if info_json["imdb_id"] is None else str(info_json["imdb_id"])
        actor_json["knownfordepartment"] = "" if info_json["known_for_department"] is None else str(
            info_json["known_for_department"])

        actor_data = json.dumps(actor_json)
        Make(xml_path=os.path.join(self.actor_path, "person.nfo"), data=actor_data).create()
