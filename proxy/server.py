#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import proxy.base as base
import proxy.ssr as SSR
from proxy.py3 import PY3

if PY3:
    import socketserver
else:
    import SocketServer as socketserver


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        config = base.get_config()
        try:
            if PY3:
                data = json.loads(base.str_auto(conn.recv(1024)).strip())
            else:
                data = json.loads(conn.recv(1024).strip())
            if 'token' not in data:
                base.err_log(301, 'socket缺少token字段')
                conn.sendall(base.get_send_buf(301))
            elif data['token'] == config['token'] is not None:
                if 'command' not in data:
                    base.err_log(302, 'socket缺少command字段')
                    conn.sendall(base.get_send_buf(302))
                elif data['command'] == 101:
                    res_data, res_status = SSR.s_101()
                    res_data = base.get_data(res_data, config['server']['host'])
                    if res_status == 201:
                        conn.sendall(base.get_send_buf(res_status, base.get_data(res_data, 'data')))
                    else:
                        conn.sendall(base.get_send_buf(res_status, base.get_data(res_data, 'err')))
                elif data['command'] == 102:
                    if 'remarks' in data:
                        res_data, res_status = SSR.s_102(data['remarks'])
                        res_data = base.get_data(res_data, config['server']['host'])
                        if res_status == 202:
                            conn.sendall(base.get_send_buf(res_status, base.get_data(res_data, 'data')))
                        else:
                            conn.sendall(base.get_send_buf(res_status, base.get_data(res_data, 'err')))
                    else:
                        base.err_log(303, 'socket缺少remarks字段')
                        conn.sendall(base.get_send_buf(303))
                else:
                    base.err_log(402, 'command不正确:' + data['command'] if data['command'] is not None else 'None')
                    conn.sendall(
                        base.get_send_buf(402, base.get_data(data['command'] if data['command'] is not None else 'None',
                                                             'err')))
            else:
                base.err_log(401, 'token不正确:' + data['token'] if data['token'] is not None else 'None')
                conn.sendall(
                    base.get_send_buf(401,
                                      base.get_data(data['token'] if data['token'] is not None else 'None', 'err')))
        except Exception:
            import traceback
            base.err_log(500, traceback.format_exc())
            conn.sendall(base.get_send_buf(500, base.get_data('未知的的异常', 'err')))
        finally:
            base.clean_group()
