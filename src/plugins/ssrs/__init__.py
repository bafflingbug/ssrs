import os
import re

import requests
import yaml
import base64
from flask import Blueprint, json, request, current_app
from .tools import safe_get, safe_value
from .ssr import SSR

blueprint = Blueprint(os.path.dirname(__file__), __name__)

path = os.path.dirname(__file__)

config = None
host = None
port = None
token = None
group = None


@blueprint.route('/')
def index():
    url_list = ssr_load()
    if url_list is None:
        return json.dumps({'code': -100, 'msg': 'not find config'})
    if 'not_base64' in request.args and request.args['not_base64'] == 1:
        return json.dumps({'code': 0, 'data': url_list, 'msg': 0})
    else:
        if len(url_list) > 0:
            ret = '\n'.join(url_list)
            return base64.urlsafe_b64encode(ret)
    return ''


@blueprint.route('/config/reload')
def config_reload():
    if load_config():
        return json.dumps({'code': 0, 'msg': ''})
    else:
        return json.dumps({'code': -100, 'msg': 'yaml decode error'})


def load_config():
    global config, host, port, group
    try:
        with open(path + '/config.yaml', 'r') as f:
            config = yaml.load(f)
        if config is None:
            return False
        host = safe_get(safe_get(config, 'server'), 'host')
        port = safe_value(safe_get(safe_get(config, 'server'), 'port'), 80)
        group = safe_value(safe_get(config, 'group'), 'default_group')
        return True
    except yaml.YAMLError:
        return False


def get_config():
    global config
    if config is None:
        if not load_config():
            return None
    return config


def ssr_load():
    global group
    conf = get_config()
    if conf is None:
        return None
    services = safe_get(conf, 'ssr')
    if services is None:
        return None
    url = []
    for service in services:
        con = safe_get(service, 'config')
        remarks = safe_value(safe_get(safe_get(config, 'ssr'), 'remarks'), 'default')
        ssr = SSR(con, group, remarks)
        url.extend(ssr.get_services())
    return url


def reg(url, host, port, token):
    requests.post(url, json=json.dumps({'token': token, 'host': host, 'port': port}))


try:
    config = get_config()
    if config is None:
        raise ValueError('not find config')
    host = safe_get(config, 'host')
    port = safe_value(safe_get(config, 'port'), 80)
    token = safe_value(safe_get(config, 'port'), '')
    if 'reg_url' in config and config['reg_url']:
        if re.match(r'^(?P<protocol>.*?)://(?P<host>[1-9a-zA-z.]*?)(?::(?P<port>\d{1,5}))?/(?P<path>.*?)?$',
                    config['reg_url']) is None:
            raise ValueError('reg_url not like protocol://host[:port]/path')
        reg(config['reg_url'], host, port)
        group = '%s'
except Exception as e:
    raise e
