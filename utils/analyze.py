#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document


class Analyze:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
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


class Make:
    def __init__(self, xml_path="./person.xml", data=""):
        self.xml_path = xml_path
        self.data = json.loads(data)

    def create(self):
        doc = Document()
        person = doc.createElement("person")
        doc.appendChild(person)
        for key in self.data:
            key_node = doc.createElement(key)
            person.appendChild(key_node)
            if "plot" == key or "outline" == key:
                value = doc.createCDATASection(str(self.data[key]))
            else:
                value = doc.createTextNode(str(self.data[key]))
            key_node.appendChild(value)
        f = open(file=self.xml_path, mode="w", encoding='UTF8')
        python_version = sys.version_info.minor
        if 8 == python_version:
            doc.writexml(writer=f, addindent="  ", newl="\n", encoding="utf-8")
        elif 8 < python_version:
            doc.writexml(writer=f, addindent="  ", newl="\n", encoding="utf-8", standalone="yes")
        f.close()
