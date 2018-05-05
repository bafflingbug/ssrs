import json
import os


def load_plugins(app):
    plugins_dir = os.path.dirname(__file__) + '/plugins/'
    with open(plugins_dir + 'plugins.json', 'r') as f:
        try:
            j = json.load(f)
        except json.JSONDecodeError as e:
            raise e
        if 'plugins' in j:
            plugins = j['plugins']
        else:
            raise Exception('plugins.json not find \'plugins\'')
    for plugin in plugins:
        p = __import__('src.plugins.%s.main' % plugin, fromlist=['blueprint'])
        app.register_blueprint(p.blueprint, url_prefix='/' + plugin)
