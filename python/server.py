#!/usr/bin/python
# -*- coding: utf-8 -*-
from python.py3 import py3
from python.base import err_log

if py3:
    import socketserver
else:
    import SocketServer as socketserver


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        while True:
            # noinspection PyBroadException
            try:
                data = int(conn.recv(10).strip())
                if data == 0:
                    pass
                elif 0 < data <= 65535:
                    pass
                else:
                    err_log('错误的socket输入:' + data)
            except:
                pass
