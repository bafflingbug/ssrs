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

    def __init__(self, conf, host, group, remarks, restart):
        self.data_list = []
        self.conf = conf
        with open(self.conf, 'r') as f:
            try:
                c = json.load(f)
                self.config = safe_get(c, "inbound")
                if self.config is None or safe_get(self.config, 'protocol') != 'vmess':
                    raise ValueError('not find vmess config')
            except Exception:
                raise ValueError('v2ray config is not json: %s' % conf)
        self.host = host
        self.group = group
        self.remarks = remarks
        self.restart = restart

    def get_services(self):
        _net = self.config['streamSettings']['network']
        _tls = self.config['streamSettings']['security']
        _path = ""
        _type = 'none'
        if _net == 'ws':
            _path = self.config['streamSettings']['network']['wsSettings']['path']
        elif _net == 'h2':
            _path = self.config['streamSettings']['network']['httpSettings']['path']
        elif _net == 'tcp':
            _type = self.config['streamSettings']['network']['tcpSettings']['header']['type']
        elif _net == 'kcp':
            _type = self.config['streamSettings']['network']['kcpSettings']['header']['type']
        elif _net == 'quic':
            _type = self.config['streamSettings']['network']['quicSettings']['header']['type']
        base_service = v2ray.Service(
            {
                'v': '2',
                'add': self.host,
                'net': _net,
                'id': self.config['settings']['clients']['id'],
                'aid': self.config['settings']['clients']['alterId'],
                'type': _type,
                'ps': self.remarks,
                'host': self.host if _net in ('ws', "h2") else "",
                'path': _path,
                'tls': _tls,
                'restart': self.restart,
                'port': self.config['port']
            }
        )
        return [base_service]
