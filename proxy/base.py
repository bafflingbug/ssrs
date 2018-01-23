#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import yaml
import json
from proxy.py3 import PY3

if PY3:
    from urllib import request
else:
    import urllib2

config = None
path = None
err_file = None
group = None


def open_auto(i_path, *k):
    if PY3:
        return open(i_path, *k, encoding='UTF-8')
    else:
        return open(i_path, *k)


def str_auto(i_bytes):
    if PY3:
        return str(i_bytes, encoding='UTF-8')
    else:
        return str(i_bytes)


def bytes_auto(i_str):
    if PY3:
        return bytes(i_str, encoding='UTF-8')
    else:
        return bytes(i_str)


def dir_path():
    global path
    if path is None:
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return path


def get_config():
    global config
    if config is None:
        with open_auto(dir_path() + '/config.yaml') as config_file:
            config = yaml.load(config_file)
    return config


def err_log(err_num, data):
    global err_file
    if err_file is None:
        err_file_open()
    err_file.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']\n错误码: ' + str(
        err_num) + '\n错误信息: ' + data + '\n')
    err_file.flush()


def err_file_open():
    global err_file
    if err_file is None:
        err_file = open_auto(dir_path() + '/error.log', 'a')
    else:
        try:
            err_file.close()
        except Exception:
            pass
        finally:
            err_file = open_auto(dir_path() + '/error.log', 'a')


def get_send_buf(status, data=None):
    if data is None:
        data = {}
    if 'status' not in data:
        data['status'] = status
    else:
        err_log(500, '构建SendBuf时存在状态码:' + str_auto(data['status']))
        data['status'] = status
    return bytes_auto(json.dumps(data))


def get_group():
    global group
    if group is not None and group != '':
        return group
    else:
        con = get_config()
        if PY3:
            res = request.urlopen(con['url'] + '/api/group.php')
        else:
            res = urllib2.urlopen(con['url'] + '/api/group.php')
        group = str_auto(res.read())
        return group


def clean_group():
    global group
    group = None


def get_data(value, key):
    return {key: value}
