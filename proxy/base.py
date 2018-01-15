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


def dir_path():
    global path
    if path is None:
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return path


def get_config():
    global config
    if config is None:
        with open(dir_path() + '/config.yaml') as config_file:
            config = yaml.load(config_file)
    return config


def err_log(err_num, data):
    global err_file
    if err_file is None:
        err_file_open()
    err_file.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']\n错误码: ' + str(
        err_num) + '\n错误信息: ' + str(data) + '\n')
    err_file.flush()


def err_file_open():
    global err_file
    if err_file is None:
        err_file = open(dir_path() + '/error.log', 'a')
    else:
        try:
            err_file.close()
        except Exception:
            pass
        finally:
            err_file = open(dir_path() + '/error.log', 'a')


def get_send_buf(status, data=None):
    if data is None:
        data = {}
    if 'status' not in data:
        data['status'] = status
    else:
        err_log(500, '构建SendBuf时存在状态码:' + str(data['status']))
        data['status'] = status
    return bytes(json.dumps(data))


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
        return str(res.read())


def get_data(value, key):
    return {key: value}
