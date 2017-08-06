# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetConfig.py  
   Description :  fetch config from config.ini
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3: get db property func
-------------------------------------------------
"""
__author__ = 'JHao'

import os
import configparser
import json
from util.utilClass import LazyProperty


class GetConfig(object):
    """
    to get config from config.ini
    """

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')
        self.config_file = configparser.ConfigParser()
        self.config_file.read(self.config_path)

    @LazyProperty
    def API_host(self):
        return self.config_file.get('API', 'host')

    @LazyProperty
    def Web_host(self):
        return self.config_file.get('Web', 'host')

    @LazyProperty
    def pytesseract_traindata(self):
        return self.config_file.get('pytesseract', 'traindata')

if __name__ == '__main__':
    gg = GetConfig()
    print (gg.API_host)