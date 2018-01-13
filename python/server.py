#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import python.base as base
from python.py3 import PY3

if PY3:
    import socketserver
else:
    import SocketServer as socketserver


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        config = base.get_config()
        while True:
            try:
                data = json.loads(str(conn.recv(1024), encoding='utf-8').strip())
                if data['token'] is None:
                    base.err_log(301, 'socket缺少token字段')
                    conn.sendall(bytes(json.dumps({'status': 301}), encoding='utf-8'))
                elif data['token'] == config['token']:
                    if data['command'] is None:
                        base.err_log(302, 'socket缺少command字段')
                        conn.sendall(bytes(json.dumps({'status': 302}), encoding='utf-8'))
                    if data['command'] == 101:
                        for ssr in config['ssr_list']:
                            pass
                        for ss in config['ss_list']:
                            pass
                    elif data['command'] == 102:
                        if data['remarks'] is not None:
                            flag = False
                            for ssr in config['ssr_list']:
                                if data['remarks'] == ssr['remarks']:
                                    pass
                            for ss in config['ss_list']:
                                if data['remarks'] == ss['remarks']:
                                    pass
                            if flag is False:
                                base.err_log(403, '未找到名为' + data + '的SS/SSR进程')
                                conn.sendall(
                                    bytes(json.dumps({'status': 403, 'err': data['remarks']}), encoding='utf-8'))
                        else:
                            base.err_log(303, 'socket缺少remarks字段')
                            conn.sendall(bytes(json.dumps({'status': 303}), encoding='utf-8'))
                    else:
                        base.err_log(402, 'command不正确')
                        conn.sendall(bytes(json.dumps({'status': 402, 'err': data['command']}), encoding='utf-8'))
                else:
                    base.err_log(401, 'token不正确:' + data['token'])
                    conn.sendall(bytes(json.dumps({'status': 401, 'err': data['token']}), encoding='utf-8'))
            except:
                import traceback
                base.err_log(500, traceback.format_exc())
                conn.sendall(bytes(json.dumps({'status': 500}), encoding='utf-8'))
