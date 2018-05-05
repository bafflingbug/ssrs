import os


def load_plugins(app):
    plugins_dir = os.path.dirname(__file__) + '/plugins/'
    plugins = os.listdir(plugins_dir)
    for plugin in plugins:
        if os.path.isdir(plugins_dir + plugin) and plugin[0:2] != '__':
            p = __import__('src.plugins.%s' % plugin, fromlist=['blueprint'])
            if p.blueprint:
                app.register_blueprint(p.blueprint, url_prefix='/' + plugin)
