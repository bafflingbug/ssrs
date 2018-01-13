#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import yaml

config = None
path = None


def dir_path():
    global path
    if path is None:
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return path


def get_config():
    global config
    if config is None:
        config_file = open(dir_path() + '/config.yaml')
        config = yaml.load(config_file)
        config_file.close()
    return config


def err_log(err_num, data):
    error_file = open(dir_path() + '/error.log', 'a')
    error_file.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']\n错误码:' + str(
        err_num) + '\n错误信息' + str(data) + '\n')
    error_file.close()
