#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import traceback
from multiprocessing import Process
import requests
import yaml
from flask import Blueprint, json, current_app, request
from .ssr import SSR

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
        ssr_list = ssr_load()
        if ssr_list is None:
            return json.dumps({'code': 100, 'msg': 'no SSR'})
        return json.dumps({'code': 0, 'data': {'data': ssr_list}, 'msg': 0})
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


def ssr_load():
    conf = get_config()
    if conf is None:
        raise ValueError('not find config')
    services = conf.get('ssr', None)
    if services is None:
        raise ValueError('not find \'ssr\' in config')
    servers = []
    for service in services:
        con = service.get('config', None)
        if not con and con == '':
            raise ValueError('SSR config not find')
        host = get_host()
        if host is None:
            raise ValueError('\'host\' is config is None')
        remarks = service.get('remarks', 'default')
        restart = service.get('restart', '')
        ssr_ = SSR(con, host, '', remarks, restart)
        servers.extend(ssr_.get_services())
    return servers


def _reg(url, h, s, t):
    global path
    time.sleep(10)
    requests.post(url, json=json.dumps({'token': t, 'url': '%s/%s/' % (s, os.path.basename(path)), 'server': h}))
    exit(0)


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
        reg_server = conf.get('reg_server', None)
        if reg_server is not None:
            p = Process(target=_reg, args=(reg_server + 'reg', host, server, token))
            p.start()
    except Exception as e:
        raise e


init()
