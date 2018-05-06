#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import requests
import yaml
import base64
from flask import Blueprint, json, request
from .tools import safe_get, safe_value
from .ssr import SSR

blueprint = Blueprint(os.path.dirname(__file__), __name__)

path = os.path.dirname(__file__)

config = None
group = None


@blueprint.route('/')
def index():
    try:
        url_list = ssr_load()
        if url_list is None:
            return json.dumps({'code': -100, 'msg': 'not find config'})
        if 'not_base64' in request.args and int(request.args['not_base64']) == 1:
            return json.dumps({'code': 0, 'data': {'url': url_list}, 'msg': 0})
        else:
            if len(url_list) > 0:
                ret = '\n'.join(url_list)
                return base64.urlsafe_b64encode(ret.encode('utf-8')).decode().rstrip('=')
        return ''
    except Exception as e:
        return json.dumps({'code': -500, 'msg': ' '.join(e.args)})


@blueprint.route('/config/reload')
def config_reload():
    if load_config():
        return json.dumps({'code': 0, 'msg': ''})
    else:
        return json.dumps({'code': -100, 'msg': 'yaml decode error'})


def load_config():
    global config
    try:
        with open(path + '/config.yaml', 'r') as f:
            config = yaml.load(f)
        if config is None:
            return False
        return True
    except yaml.YAMLError:
        return False


def get_config():
    global config
    if config is None:
        if not load_config():
            return None
    return config


def get_host():
    conf = get_config()
    host = safe_get(conf, 'host')
    return host


def ssr_load():
    g = get_group()
    conf = get_config()
    if conf is None:
        return None
    services = safe_get(conf, 'ssr')
    if services is None:
        return None
    url = []
    for service in services:
        con = safe_get(service, 'config')
        host = get_host()
        if host is None:
            raise ValueError('\'host\' is config is None')
        remarks = safe_value(safe_get(safe_get(config, 'ssr'), 'remarks'), 'default')
        restart = safe_value(safe_get(safe_get(config, 'ssr'), 'restart'), '')
        ssr = SSR(con, host, g, remarks, restart)
        url.extend(ssr.get_services())
    return url


def reg(url, h, p, t):
    requests.post(url, json=json.dumps({'token': t, 'host': h, 'port': p}))


def get_group_from_url(url):
    req = requests.get(url)
    j = req.json()
    if 'code' not in j and j['code'] != 0:
        return 'default_group'
    else:
        try:
            return j['data']['group']
        except IndexError:
            return 'default_group'


def set_group(g):
    global group
    group = g


def get_group():
    global group
    return group if group else 'default_group'


def init():
    try:
        conf = get_config()
        if conf is None:
            raise ValueError('not find config')
        host = get_host()
        if host is None:
            raise ValueError('\'host\' is config is None')
        port = safe_value(safe_get(conf, 'port'), 80)
        token = safe_value(safe_get(conf, 'port'), '')
        if 'reg_server' in conf and conf['reg_server']:
            if re.match(r'^(?P<protocol>.*?)://(?P<host>[1-9a-zA-z.]*?)(?::(?P<port>\d{1,5}))?/(?P<path>.*?)?$',
                        conf['reg_url']) is None:
                raise ValueError('reg_url not like protocol://host[:port]/path')
            reg(conf['reg_server'] + 'reg', host, port, token)
            g = get_group_from_url(conf['reg_server'] + 'group')
            set_group(g)
        else:
            set_group(safe_value(safe_get(conf, 'group'), 'default_group'))
    except Exception as e:
        raise e
