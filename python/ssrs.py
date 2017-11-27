import base64
import json
import hashlib
from network import *

def new_config(file, fileMD5):
    config_file = open(file, 'rb')
    md5 = hashlib.md5(config_file.read()).hexdigest()
    config_file.close()
    if file in fileMD5.keys() and fileMD5[file] == md5:
        return False
    fileMD5[file] = md5
    return True


def ssr2URL(ssr, config, group):
    ssr_config_file = open(ssr['config-file'], 'r')
    ssr_config = json.load(ssr_config_file)
    param_str = "obfsparam=" + base64.urlsafe_b64encode(ssr_config['obfs_param'].encode() if not ssr_config['obfs_param'] is None else ''.encode()).decode().rstrip('=')
    if 'protocol_param' in ssr_config.keys() and (not ssr_config['protocol_param'] == ""):
        param_str += '&protoparam=' + base64.urlsafe_b64encode(ssr_config['protocol_param'].encode()).decode().rstrip('=')
    if 'remarks' in ssr.keys() and (not ssr['remarks'] == ""):
        param_str += '&remarks=' + base64.urlsafe_b64encode(ssr['remarks'].encode()).decode().rstrip('=')
    param_str += '&group=' + base64.urlsafe_b64encode(group.encode()).decode().rstrip('=')
    main_part = config["host"] + ':' + str(ssr_config['server_port']) + ':' + ssr_config['protocol'] + ':' + ssr_config['method'] + ':' + ssr_config['obfs'] + ':' + base64.urlsafe_b64encode(ssr_config['password'].encode()).decode().rstrip('=')
    ssr_config_file.close()
    b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
    return 'ssr://' + b64 + '\n'


def ss2URL(ss, config, group):
    ss_config_file = open(ss['config-file'], 'r')
    ss_config = json.load(ss_config_file)
    param_str = "obfsparam=" + ''
    if 'remarks' in ss.keys() and (not ss['remarks'] == ""):
        param_str += '&remarks=' + base64.urlsafe_b64encode(ss['remarks'].encode()).decode().rstrip('=')
    param_str += '&group=' + base64.urlsafe_b64encode(group.encode()).decode().rstrip('=')
    main_part = config["host"] + ':' + str(ss_config['server_port']) + ':' + 'origin' + ':' + ss_config['method'] + ':' + 'plain' + ':' + base64.urlsafe_b64encode(ss_config['password'].encode()).decode().rstrip('=')
    ss_config_file.close()
    b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
    return 'ssr://' + b64 + '\n'
