#!/usr/bin/python
# -*- coding: utf-8 -*-
import python.server as server
from python.py3 import py3
from python.base import get_config

if __name__ == '__main__':
    if not py3:
        import sys

        reload(sys)
        sys.setdefaultencoding('utf-8')
    config = get_config()
    server = server.socketserver.ThreadingTCPServer((config['server']['host'], config['server']['port']),
                                                    server.Handler)
    server.serve_forever()
