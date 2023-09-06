#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


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
