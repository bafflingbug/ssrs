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
    log_file = None
    try:
        log_file = open(dir_path + '/log.json', 'r')
        logfile = json.load(log_file)
    except:
        logfile = {}
        update = True
    finally:
        if log_file:
            log_file.close()
    u = new_config(dir_path + '/config.json', logfile)
    update = u if not update else update
    config_file = open(dir_path + '/config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    group = getgroup('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/group.php')
    if 'group' not in logfile.keys() or group != logfile['group']:
        print(group)
        update = True
        logfile['group'] = group

    ssr_url = ''

    for ss_config in config['ss-config-file']:
        u = new_config(ss_config['config-file'], logfile)
        update = u if not update else update
        url = ss2URL(ss_config, config, group)
        if url is not False:
            ssr_url += url
            if 'port' not in logfile[ss_config['config-file']].keys() or logfile[ss_config['config-file']]['port'] is not True:
                update = True
                logfile[ss_config['config-file']]['port'] = True
        else:
            if 'port' not in logfile[ss_config['config-file']].keys() or logfile[ss_config['config-file']]['port'] is not False:
                update = True
                logfile[ss_config['config-file']]['port'] = False

    for ssr_config in config['ssr-config-file']:
        u = new_config(ssr_config['config-file'], logfile)
        update = u if not update else update
        url = ssr2URL(ssr_config, config, group)
        if url is not False:
            ssr_url += url
            if 'port' not in logfile[ssr_config['config-file']].keys() or logfile[ssr_config['config-file']]['port'] is not True:
                update = True
                logfile[ssr_config['config-file']]['port'] = True
        else:
            if 'port' not in logfile[ssr_config['config-file']].keys() or logfile[ssr_config['config-file']]['port'] is not False:
                update = True
                logfile[ssr_config['config-file']]['port'] = False
    if update:
        print('post')
        print(ssr_url)
        MD5_file = open(dir_path + '/log.json', 'w')
        json.dump(logfile, MD5_file)
        MD5_file.close()
        res = post('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/post.php', ssr_url,
                   config['token'], config['host'])
    else:
        print('active')
        state = active('http://' if not config['ssl'] else 'https://' + config['main-server'] + '/active.php', config['token'], config['host'])
        if state.find('error:2') >= 0:
            MD5_file = open(dir_path + '/log.json', 'w')
            MD5_file.truncate()
            MD5_file.close()
            os.system('python ' + dir_path + '/ssrs.py')
