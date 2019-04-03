# !/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import copy
import socket
import subprocess

from .tools import safe_get, safe_value


class v2ray:
    class Service:
        def __init__(self, conf):
            self.conf = conf

        def update(self, array):
            self.conf.update(array)

        def port_open(self, first=True):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for i in range(2):
                try:
                    s.connect(('127.0.0.1', int(self.conf['port'])))
                    s.shutdown(2)
                    return True
                except socket.error:
                    if first:
                        self.restart()
                        return self.port_open(first=False)
                    return False
            return False

        def restart(self):
            return subprocess.call(self.conf['restart'], shell=True)

        def get_data(self):
            if not self.port_open():
                return None
            return base64.urlsafe_b64encode(json.dumps(self.conf).encode()).decode()

    def __init__(self, conf, tips, host, remarks, restart):
        self.data_list = []
        self.conf = conf
        with open(self.conf, 'r') as f:
            try:
                self.configs = json.load(f)
                # self.config = safe_get(c, "inbound")
                # if self.config is None or safe_get(self.config, 'protocol') != 'vmess':
                #     raise ValueError('not find vmess config')
            except Exception:
                raise ValueError('v2ray config is not json: %s' % conf)
        self.host = host
        self.remarks = remarks
        self.restart = restart
        self.tips = tips

    def get_services(self):
        if safe_get(self.configs, 'inbounds') is not None:
            c = safe_get(self.configs, 'inbounds')
        elif safe_get(self.configs, 'inbound') is not None:
            c = [safe_get(self.configs, 'inbound')]
        else:
            raise ValueError('not find vmess config')
        for config in c:
            if config['protocol'] != 'vmess':
                continue
            _net = config['streamSettings']['network']
            _path = ""
            _type = 'none'
            if _net == 'ws':
                _path = config['streamSettings']['wsSettings']['path']
            elif _net == 'h2':
                _path = config['streamSettings']['httpSettings']['path']
            elif _net == 'tcp':
                _type = config['streamSettings']['tcpSettings']['header']['type']
            elif _net == 'kcp':
                _type = config['streamSettings']['kcpSettings']['header']['type']
            elif _net == 'quic':
                _type = config['streamSettings']['quicSettings']['header']['type']
            base_service = v2ray.Service(
                {
                    'v': '2',
                    'add': self.host,
                    'net': _net,
                    'id': '',
                    'aid': 0,
                    'type': _type,
                    'ps': self.remarks,
                    'host': self.host if _net in ('ws', "h2") else "",
                    'path': _path,
                    'tls': config['streamSettings']['security'],
                    'restart': self.restart,
                    'port': config['port']
                }
            )
            _port = config['port']
            if int(_port) in self.tips:
                base_service.update(self.tips[int(_port)])
            for item in config['settings']['clients']:
                service = copy.deepcopy(base_service)
                a = {
                    'id': item['id'],
                    'aid': item['alterId']
                }
                service.update(a)
                url = service.get_data()
                if url is None:
                    continue
                self.data_list.append(url)
        return self.data_list
