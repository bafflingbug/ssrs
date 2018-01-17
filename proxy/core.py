#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time
import proxy.server as server
from proxy.py3 import PY3
import proxy.base as base
import proxy.reg as reg


def reg_thread():
    time.sleep(20)
    reg.reg()


def server_thread():
    config = base.get_config()
    ser = server.socketserver.ThreadingTCPServer((config['server']['host'], config['server']['port']),
                                                 server.Handler)
    ser.serve_forever()


if __name__ == '__main__':
    if not PY3:
        import sys

        reload(sys)
        sys.setdefaultencoding('utf-8')
    while True:
        ts = threading.Thread(target=server_thread)
        ts.setDaemon(True)
        ts.start()
        tr = threading.Thread(target=reg_thread)
        tr.setDaemon(True)
        tr.start()
        tr.join()
        ts.join()
