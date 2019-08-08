# !/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import copy
import socket
import subprocess
import six


class SSR:
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
            if 'restart' in self.conf:
                return subprocess.call(self.conf['restart'], shell=True)
            return

        def get_data(self):
            if not self.port_open():
                return None
            self.conf.pop('restart')
            return base64.urlsafe_b64encode(json.dumps(self.conf).encode()).decode()

    def __init__(self, conf, host, group, remarks, restart):
        self.data_list = []
        self.conf = conf
        with open(self.conf, 'r') as f:
            try:
                self.config = json.load(f)
            except Exception:
                raise ValueError('SSR config is not json: %s' % conf)
        self.host = host
        self.group = group
        self.remarks = remarks
        self.restart = restart

    def get_services(self):
        if ('server_port' not in self.config or 'password' not in self.config) and 'port_password' not in self.config:
            raise KeyError('SSR config is incorrect')
        base_service = SSR.Service(
            {
                'host': self.host,
                'protocol': self.config.get('protocol', 'origin'),
                'protoparam': self.config.get('protocol_param', ''),
                'method': self.config.get('method', 'none'),
                'obfs': self.config.get('obfs', 'plain'),
                'obfsparam': self.config.get('obfs_param', ''),
                'remarks': self.remarks,
                'group': self.group,
                'restart': self.restart,
                'password': '',
                'port': 0
            }
        )
        if 'port_password' in self.config:
            for port, data in six.iteritems(self.config['port_password']):
                service = copy.deepcopy(base_service)
                if type(data) is str:
                    array = {'password': data}
                elif type(data) is dict:
                    array = data
                else:
                    continue
                array['remarks'] = self.remarks + ('_%s' % str(port))
                array['port'] = port
                service.update(array)
                url = service.get_data()
                if url is None:
                    continue
                self.data_list.append(url)
        else:
            base_service.update({'port': self.config['server_port'], 'password': self.config['password']})
            url = base_service.get_data()
            if url is not None:
                self.data_list.append(url)
        return self.data_list
