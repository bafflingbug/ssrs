# !/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import copy
import socket

from .tools import safe_get, safe_value


class SSR:
    class Service:
        def __init__(self, conf):
            self.conf = conf

        def update(self, array):
            self.conf.update(array)

        def port_open(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', int(self.conf['port'])))
                s.shutdown(2)
                return True
            except socket.error:
                return False

        def get_url(self):
            if not self.port_open():
                return ''
            param_str = 'obfsparam=' + base64.urlsafe_b64encode(self.conf['obfsparam'].encode()).decode().rstrip('=')
            if self.conf['protoparam'] != '':
                param_str += '&protoparam=' + base64.urlsafe_b64encode(
                    self.conf['protoparam'].encode()).decode().rstrip('=')
            if self.conf['remarks'] != '':
                param_str += '&remarks=' + base64.urlsafe_b64encode(self.conf['remarks'].encode()).decode().rstrip('=')
            param_str += '&group=' + base64.urlsafe_b64encode(self.conf['group'].encode()).decode().rstrip('=')
            main_part = self.conf['host'] + ':' + str(self.conf['port']) + ':' + self.conf[
                'protocol'] + ':' + self.conf['method'] + ':' + self.conf['obfs'] + ':' + base64.urlsafe_b64encode(
                self.conf['password'].encode()).decode().rstrip('=')
            b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
            return 'ssr://' + b64

    def __init__(self, conf, host, group, remarks, restart):
        self.url_list = []
        self.conf = conf
        with open(self.conf, 'r') as f:
            try:
                self.config = json.load(f)
            except json.JSONDecodeError:
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
                'protocol': safe_value(safe_get(self.config, 'protocol'), 'origin'),
                'protoparam': safe_value(safe_get(self.config, 'protocol_param'), ''),
                'method': safe_value(safe_get(self.config, 'method'), 'none'),
                'obfs': safe_value(safe_get(self.config, 'obfs'), 'plain'),
                'obfsparam': safe_value(safe_get(self.config, 'obfs_param'), ''),
                'remarks': self.remarks,
                'group': self.group,
                'restart': self.restart,
                'password': '',
                'port': 0
            }
        )
        if 'port_password' in self.config:
            for port, array in self.config['port_password'].items():
                service = copy.deepcopy(base_service)
                array['remarks'] = self.remarks + ('_%d' % port)
                array['port'] = port
                service.update(array)
                url = service.get_url()
                if url is None:
                    continue
                self.url_list.append(url)
        else:
            base_service.update({'port': self.config['server_port'], 'password': self.config['password']})
            url = base_service.get_url()
            if url is not None:
                self.url_list.append(url)
        return self.url_list
