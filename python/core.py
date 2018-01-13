#!/usr/bin/python
# -*- coding: utf-8 -*-
import python.server as server
from python.py3 import PY3
import python.base as base
import python.reg as reg

if __name__ == '__main__':
    if not PY3:
        import sys

        reload(sys)
        sys.setdefaultencoding('utf-8')
    reg.reg()
    config = base.get_config()
    server = server.socketserver.ThreadingTCPServer((config['server']['host'], config['server']['port']),
                                                    server.Handler)
    server.serve_forever()
