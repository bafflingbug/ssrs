import os
import yaml
import base64
from flask import Blueprint, json, request

blueprint = Blueprint(os.path.dirname(__file__), __name__)

path = os.path.dirname(__file__)

config = None


@blueprint.route('/')
def index():
    config = get_config()
    if config is None:
        return json.dumps({'code': -100, 'msg': 'not find config'})
    url_list = ssr_load(config)
    if len(url_list) == 0:
        return ''
    else:
        ret = '\n'.join(url_list)
    if 'not_base64' in request.args and request.args['not_base64'] == 1:
        return ret
    else:
        return base64.urlsafe_b64encode(ret)


@blueprint.route('/config/reload')
def config_reload():
    if load_config():
        return json.dumps({'code': 0, 'msg': ''})
    else:
        return json.dumps({'code': -100, 'msg': 'yaml decode error'})


def load_config():
    global config
    try:
        config = yaml.safe_load(path + 'config.yaml')
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


def ssr_load():
    pass
