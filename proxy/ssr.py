#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import json
import base64
import subprocess
import proxy.base as base


def restart(res):
    return subprocess.call(res, shell=True)


def port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', int(port)))
        s.shutdown(2)
        print('%d is open' % port)
        return True
    except:
        print('%d is down' % port)
        return False


def all():
    config = base.get_config()
    remarks = set()
    data = dict()
    for ssr in config['ssr_list']:
        if ssr['remarks'] not in remarks:
            remarks.add(ssr['remarks'])
            ssrurl = ssr2URL(ssr)
            if ssrurl is not False:
                data[ssr['remarks']] = ssrurl
        else:
            base.err_log(502, '存在相同remarks的SS/SSR进程:' + ssr['remarks'])
    for ss in config['ss_list']:
        if ss['remarks'] not in remarks:
            remarks.add(ss['remarks'])
            ssurl = ss2URL(ss)
            if ssurl is not False:
                data[ss['remarks']] = ssurl
        else:
            base.err_log(502, '存在相同remarks的SS/SSR进程:' + ss['remarks'])
    return data


def ssr2URL(ssr):
    group = base.get_group()
    config = base.get_config()
    with base.open_auto(ssr['config_file'], 'r') as ssr_config_file:
        ssr_config = json.load(ssr_config_file)
    if not port_open(ssr_config['server_port']):
        restart(ssr['restart'])
        if not port_open(ssr_config['server_port']):
            base.err_log(501, 'SSR进程无法运行:' + ssr['remarks'])
            return False
    param_str = 'obfsparam=' + base64.urlsafe_b64encode(
        ssr_config['obfs_param'].encode() if not ssr_config['obfs_param'] is None else ''.encode()).decode().rstrip('=')
    if 'protocol_param' in ssr_config.keys() and (not ssr_config['protocol_param'] == ''):
        param_str += '&protoparam=' + base64.urlsafe_b64encode(ssr_config['protocol_param'].encode()).decode().rstrip(
            '=')
    if 'remarks' in ssr.keys() and not ssr['remarks'] == '':
        param_str += '&remarks=' + base64.urlsafe_b64encode(ssr['remarks'].encode()).decode().rstrip('=')
    param_str += '&group=' + base64.urlsafe_b64encode(group.encode()).decode().rstrip('=')
    main_part = config['server']['host'] + ':' + str(ssr_config['server_port']) + ':' + ssr_config[
        'protocol'] + ':' + ssr_config['method'] + ':' + ssr_config['obfs'] + ':' + base64.urlsafe_b64encode(
        ssr_config['password'].encode()).decode().rstrip('=')
    b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
    return 'ssr://' + b64 + '\n'


def ss2URL(ss):
    group = base.get_group()
    config = base.get_config()
    with base.open_auto(ss['config_file'], 'r') as ss_config_file:
        ss_config = json.load(ss_config_file)
    if not port_open(ss_config['server_port']):
        restart(ss['restart'])
        if not port_open(ss_config['server_port']):
            base.err_log(501, 'SS进程无法运行:' + ss['remarks'])
            return False
    param_str = 'obfsparam=' + ''
    if 'remarks' in ss.keys() and not ss['remarks'] == '':
        param_str += '&remarks=' + base64.urlsafe_b64encode(ss['remarks'].encode()).decode().rstrip('=')
    param_str += '&group=' + base64.urlsafe_b64encode(group.encode()).decode().rstrip('=')
    main_part = config['server']['host'] + ':' + str(ss_config['server_port']) + ':' + 'origin' + ':' + \
                ss_config['method'] + ':' + 'plain' + ':' + base64.urlsafe_b64encode(
        ss_config['password'].encode()).decode().rstrip('=')
    b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
    return 'ssr://' + b64 + '\n'
