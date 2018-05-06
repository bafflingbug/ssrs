#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def load_plugins(app):
    plugins_dir = os.path.dirname(__file__) + '/plugins/'
    plugins = os.listdir(plugins_dir)
    for plugin in plugins:
        if os.path.isdir(plugins_dir + plugin) and plugin[0:2] != '__':
            try:
                p = __import__('plugins.%s' % plugin, fromlist=['blueprint'])
            except ImportError as e:
                app.logger.error('Error on load plugin %s' % plugin)
                print(e)
                return
            if p and p.blueprint:
                try:
                    app.register_blueprint(p.blueprint, url_prefix='/' + plugin)
                except TypeError:
                    app.logger.error('%s.blueprint is not a flask.Blueprint' % plugin)
                app.logger.info('Success load plugin %s' % plugin)
