import json
import os
from network import *
from ssrs import *
import sys

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    update = False
    dir_path = os.path.dirname(os.path.realpath(__file__))
    MD5_file = None
    try:
        MD5_file = open(dir_path + '/MD5.json', 'r')
        fileMD5 = json.load(MD5_file)
    except:
        fileMD5 = {}
        update = True
    finally:
        if MD5_file:
            MD5_file.close()
    update = new_config(dir_path + '/config.json', fileMD5, update)
    config_file = open(dir_path + '/config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    group = getgroup('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/group.php')
    if 'group' not in fileMD5.keys() or group != fileMD5['group']:
        print(group)
        update = True
        fileMD5['group'] = group
    ssr_url = ''
    for ss_config in config['ss-config-file']:
        update = new_config(ss_config['config-file'], fileMD5, update)
        ssr_url += ss2URL(ss_config, config, group)
    for ssr_config in config['ssr-config-file']:
        update = new_config(ssr_config['config-file'], fileMD5, update)
        ssr_url += ssr2URL(ssr_config, config, group)
    if update:
        print(ssr_url)
        MD5_file = open(dir_path + '/MD5.json', 'w')
        json.dump(fileMD5, MD5_file)
        MD5_file.close()
        res = post('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/post.php', ssr_url,
                   config['token'], config['host'])
    else:
        state = active('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/active.php', config['token'], config['host'])
        if state.find('error:2') >= 0:
            MD5_file = open(dir_path + '/MD5.json', 'w')
            MD5_file.truncate()
            MD5_file.close()
            os.system('python ' + dir_path + '/ssrs.py')
