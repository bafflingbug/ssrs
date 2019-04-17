#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import all_feature_names
from gevent import monkey

monkey.patch_all()

import logging
import os
from flask import Flask
from service.core import load_plugins

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/flask.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)

load_plugins(app)

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer

    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
