#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from core import load_plugins

app = Flask(__name__)
load_plugins(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
