#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import python.base as base
import python.ssr as SSR
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
                if 'token' not in data:
                    base.err_log(301, 'socket缺少token字段')
                    conn.sendall(base.get_send_buf(301))
                elif data['token'] == config['token'] is not None:
                    if 'command' not in data:
                        base.err_log(302, 'socket缺少command字段')
                        conn.sendall(base.get_send_buf(302))
                    elif data['command'] == 101:
                        data = base.get_data(SSR.all(), 'data')
                        conn.sendall(base.get_send_buf(201, data))
                    elif data['command'] == 102:
                        if 'remarks' in data:
                            if data['remarks'] is not None:
                                flag = False
                                for ssr in config['ssr_list']:
                                    if data['remarks'] == ssr['remarks']:
                                        flag = True
                                        ssrurl = SSR.ssr2URL(ssr)
                                        if ssrurl is not False:
                                            ssrdata = base.get_data(base.get_data(ssrurl, ssr['remarks']), 'data')
                                            conn.sendall(base.get_send_buf(202, ssrdata))
                                        else:
                                            conn.sendall(base.get_send_buf(501,
                                                                           base.get_data('SSR进程无法运行:' + ssr['remarks'],
                                                                                         'err')))
                                        break
                                if flag is False:
                                    for ss in config['ss_list']:
                                        if data['remarks'] == ss['remarks']:
                                            flag = True
                                            ssurl = SSR.ssr2URL(ss)
                                            if ssurl is not False:
                                                ssdata = base.get_data(base.get_data(ssurl, ss['remarks']), 'data')
                                                conn.sendall(base.get_send_buf(202, ssdata))
                                            else:
                                                conn.sendall(
                                                    base.get_send_buf(501, base.get_data('SS进程无法运行:' + ss['remarks'],
                                                                                         'err')))
                                            break
                                if flag is False:
                                    base.err_log(403, '未找到名为' + data['remarks'] + '的SS/SSR进程')
                                    conn.sendall(base.get_send_buf(403, base.get_data(data['remarks'], 'err')))
                            else:
                                base.err_log(403, '未找到名为None的SS/SSR进程')
                                conn.sendall(base.get_send_buf(403, base.get_data('None', 'err')))
                        else:
                            base.err_log(303, 'socket缺少remarks字段')
                            conn.sendall(base.get_send_buf(303))
                    else:
                        base.err_log(402, 'command不正确:' + data['command'] if data['command'] is not None else 'None')
                        conn.sendall(
                            base.get_send_buf(402,
                                              base.get_data(data['command'] if data['command'] is not None else 'None',
                                                            'err')))
                else:
                    base.err_log(401, 'token不正确:' + data['token'] if data['token'] is not None else 'None')
                    conn.sendall(
                        base.get_send_buf(401,
                                          base.get_data(data['token'] if data['token'] is not None else 'None', 'err')))
            except (ConnectionAbortedError, json.decoder.JSONDecodeError):
                pass
            except:
                import traceback
                base.err_log(500, traceback.format_exc())
                conn.sendall(base.get_send_buf(500, base.get_data('未知的的异常', 'err')))
