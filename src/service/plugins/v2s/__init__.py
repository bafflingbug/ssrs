#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import traceback
from multiprocessing import Process
import requests
import yaml
import six
from flask import Blueprint, json, current_app, request
from .v2ray import V2ray

path = os.path.dirname(os.path.abspath(__file__))
blueprint = Blueprint(os.path.basename(path), __name__)

config = None


@blueprint.route('/')
def index():
    try:
        conf = get_config()
        if conf is None:
            return json.dumps({'code': -500, 'msg': 'no config'})
        if request.args.get('token', '') != conf.get('token', ''):
            return json.dumps({'code': -101, 'msg': 'token error'})
        v2_list = v2_load()
        if v2_list is None:
            return json.dumps({'code': 100, 'msg': 'no v2ray'})
        return json.dumps({'code': 0, 'data': {'data': v2_list}, 'msg': 0})
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return json.dumps({'code': -500, 'msg': repr(e)})


@blueprint.route('/config/reload')
def config_reload():
    if load_config():
        return json.dumps({'code': 0, 'msg': ''})
    else:
        return json.dumps({'code': -100, 'msg': 'yaml decode error'})


@blueprint.route('/reg')
def reg():
    init()
    return json.dumps({'code': 0, 'msg': ''})


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
    host = conf.get('host', None)
    return host


def v2_load():
    conf = get_config()
    if conf is None:
        raise ValueError('not find config')
    services = conf.get('v2ray', None)
    if services is None:
        raise ValueError('not find \'v2ray\' in config')
    servers = []
    for service in services:
        con = service.get('config', None)
        ctips = service.get('tips', None)
        tips = {}
        if ctips is not None:
            for item in ctips:
                oport = item['origin_port']
                i = {}
                for k, v in six.iteritems(item):
                    if k != 'origin_port':
                        i[k] = v
                tips[int(oport)] = i
        if not con and con == '':
            raise ValueError('v2ray config not find')
        host = get_host()
        if host is None:
            raise ValueError('\'host\' is config is None')
        remarks = service.get('remarks', 'default')
        restart = service.get('restart', '')
        v2 = V2ray(con, tips, host, remarks, restart)
        servers.extend(v2.get_services())
    return servers


def _reg(url, h, s, t):
    global path
    time.sleep(10)
    requests.post(url, json=json.dumps({'token': t, 'url': '%s/%s/' % (s, os.path.basename(path)), 'server': h}))
    exit(0)


def get_group(url):
    req = requests.get(url)
    if not req:
        return 'default_group'
    j = req.json()
    if 'code' not in j and j['code'] != 0:
        return 'default_group'
    else:
        try:
            return j['data']['group']
        except IndexError:
            return 'default_group'


def init():
    try:
        conf = get_config()
        if conf is None:
            raise ValueError('not find config')
        host = get_host()
        if host is None:
            raise ValueError('\'host\' is config is None')
        server = conf.get('server', 'http://127.0.0.1:80')
        token = conf.get('token', '')
        if 'reg_server' in conf and conf['reg_server']:
            p = Process(target=_reg, args=(conf['reg_server'] + 'reg', host, server, token))
            p.start()
    except Exception as e:
        raise e


init()
