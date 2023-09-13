#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
from utils.analyze import Make
import utils.DateUtil as DateUtil

# https://api.tmdb.org
# https://tmdb.nastool.org
# https://t.nastool.workers.dev
# https://api.themoviedb.org
api_url = "https://api.tmdb.org"
image_url = "https://image.tmdb.org"


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
        if 200 == response.status_code:
            return response.text.encode("utf-8")
        else:
            return "{}"

    def get_actor_image(self):
        ac_json = json.loads(self.get_actor_info())
        if len(ac_json.keys()) > 0:
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
        if 200 == response.status_code:
            return response.text
        else:
            return "{}"

    def get_actor_plot(self):
        plot = ""
        translations = self.__translations()
        translations_json = json.loads(translations)
        if "translations" in translations_json:
            translations_list = json.loads(translations)["translations"]
            translations_json = {}
            for translation in translations_list:
                translations_json[translation["iso_3166_1"]] = translation
            if "CN" in translations_json.keys():
                zh = translations_json["CN"]
                plot = zh["data"]["biography"]
            elif "US" in translations_json.keys():
                us = translations_json["US"]
                plot = us["data"]["biography"]
            else:
                default_value = translations_json[0]
                plot = default_value["data"]["biography"]
            plot = plot.replace("\n", "").replace("\r\n", "")
        return plot

    def create_actor_nfo(self, redo=False):
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
        if len(info_json.keys()) > 0:
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
            # 不建议使用，存在gbk转码问题
            # actor_json["alsoknownas"] = "" if info_json["also_known_as"] is None else info_json["also_known_as"]
            actor_json["deathday"] = "" if info_json["deathday"] is None else str(info_json["deathday"])
            actor_json["gender"] = "" if info_json["gender"] is None else str(info_json["gender"])
            actor_json["homepage"] = "" if info_json["homepage"] is None else str(info_json["homepage"])
            actor_json["imdbid"] = "" if info_json["imdb_id"] is None else str(info_json["imdb_id"])
            actor_json["knownfordepartment"] = "" if info_json["known_for_department"] is None else str(
                info_json["known_for_department"])

            actor_data = json.dumps(actor_json)
            person_nfo = os.path.join(self.actor_path, "person.nfo")
            try:
                Make(xml_path=person_nfo, data=actor_data).create()
                # 重做模式下删除重新成功刮削的信息
                if redo:
                    error_file_read = open("./error_tmdb_ids.txt", "r+")
                    new_read = error_file_read.read().replace(os.path.basename(self.actor_path) + ",", "")
                    error_file_w = open("./error_tmdb_ids.txt", "w")
                    error_file_w.write(new_read)
                    error_file_w.close()
            except Exception as e:
                os.remove(person_nfo)
                # 非重做模式下记录刮削异常信息，重做模式下不再重复记录
                if not redo:
                    error_file = open("../error_tmdb_ids.txt", "w+")
                    error_file.write(os.path.basename(self.actor_path) + ",")
                    error_file.close()
                self.log.logger.error(actor_data)
                self.log.logger.error("当前写入元数据出现异常，路径:{0}, 异常:{1}".format(self.actor_path, e))
