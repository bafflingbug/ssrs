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
                if 'token' not in data or data['token'] is None:
                    base.err_log(301, 'socket缺少token字段或者为None')
                    conn.sendall(base.get_send_buf(301))
                elif data['token'] == config['token']:
                    if 'command' not in data or data['command'] is None:
                        base.err_log(302, 'socket缺少command字段或者为None')
                        conn.sendall(base.get_send_buf(302))
                    if data['command'] == 101:
                        for ssr in config['ssr_list']:
                            pass
                        for ss in config['ss_list']:
                            pass
                    elif data['command'] == 102:
                        if 'remarks' in data or data['remarks'] is not None:
                            flag = False
                            for ssr in config['ssr_list']:
                                if data['remarks'] == ssr['remarks']:
                                    pass
                            for ss in config['ss_list']:
                                if data['remarks'] == ss['remarks']:
                                    pass
                            if flag is False:
                                base.err_log(403, '未找到名为' + data['remarks'] + '的SS/SSR进程')
                                conn.sendall(base.get_send_buf(403, {'err': data['remarks']}))
                        else:
                            base.err_log(303, 'socket缺少remarks字段或者为None')
                            conn.sendall(base.get_send_buf(303))
                    else:
                        base.err_log(402, 'command不正确')
                        conn.sendall(base.get_send_buf(402, {'err': data['command']}))
                else:
                    base.err_log(401, 'token不正确:' + data['token'])
                    conn.sendall(base.get_send_buf(401, {'err': data['token']}))
            except (ConnectionAbortedError, json.decoder.JSONDecodeError):
                pass
            except:
                import traceback
                base.err_log(500, traceback.format_exc())
                conn.sendall(base.get_send_buf(500))
