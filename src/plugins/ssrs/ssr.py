import base64
import json
import copy
from .tools import safe_get, safe_value


class SSR:
    class Service:
        def __init__(self, conf):
            self.conf = conf

        def update(self, port, array):
            self.conf['port'] = port
            self.conf.update(array)

        def get_url(self):
            param_str = 'obfsparam=' + base64.urlsafe_b64encode(self.conf['obfsparam'].encode()).decode().rstrip('=')
            if self.conf['protocolparam'] != '':
                param_str += '&protoparam=' + base64.urlsafe_b64encode(self.conf['protocolparam'].encode()).decode().rstrip('=')
            if self.conf['remarks'] != '':
                param_str += '&remarks=' + base64.urlsafe_b64encode(self.conf['remarks'].encode()).decode().rstrip('=')
            param_str += '&group=' + base64.urlsafe_b64encode(self.conf['group'].encode()).decode().rstrip('=')
            main_part = self.conf['host'] + ':' + str(self.conf['port']) + ':' + self.conf[
                'protocol'] + ':' + self.conf['method'] + ':' + self.conf['obfs'] + ':' + base64.urlsafe_b64encode(
                self.conf['password'].encode()).decode().rstrip('=')
            b64 = base64.urlsafe_b64encode((main_part + '/?' + param_str).encode()).decode().rstrip('=')
            return 'ssr://' + b64 + '\n'

    def __init__(self, conf, group, remarks):
        self.url_list = []
        self.conf = conf
        with open(self.conf, 'r') as f:
            try:
                self.config = json.load(f)
            except json.JSONDecodeError:
                raise ValueError('SSR config is not json: %s' % conf)
        self.group = group
        self.remarks = remarks

    def get_services(self):
        if ('port' not in self.config and 'password' not in self.config) or 'port_password' not in self.config:
            raise KeyError('SSR config is incorrect')
        server = safe_get(safe_get(self.config, 'server'), 'host')
        if not server:
            raise KeyError('not find server in config')
        base_service = SSR.Service(
            {
                'server': server,
                'protocol': safe_value(safe_get(self.config, 'protocol'), 'origin'),
                'protoparam': safe_value(safe_get(self.config, 'protocol_param'), ''),
                'method': safe_value(safe_get(self.config, 'method'), 'none'),
                'obfs': safe_value(safe_get(self.config, 'obfs'), 'plain'),
                'obfsparam': safe_value(safe_get(self.config, 'obfs_param'), ''),
                'remarks': self.remarks,
                'group': self.group,
                'password': '',
                'port': 0
            }
        )
        if 'port_password' in self.config:
            for port, array in self.config['port_password'].items():
                service = copy.deepcopy(base_service)
                array['remarks'] = self.remarks + ('_%d' % port)
                service.update(port, array)
                self.url_list.append(service.get_url())
        else:
            base_service.update(self.config['server_port'], {'password': self.config['password']})
            self.url_list.append(base_service.get_url())
        return self.url_list
