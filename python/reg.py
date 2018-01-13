#!/usr/bin/python
# -*- coding: utf-8 -*-
from python.py3 import PY3
import python.base as base

if PY3:
    from urllib import request, parse
else:
    import urllib
    import urllib2


def reg():
    config = base.get_config()
    if PY3:
        data = parse.urlencode({'port': config['server']['port'], "host": config['server']['host']}).encode('utf-8')
        req = request.Request(config['url'] + '/api/reg.php', data=data)
        res = request.urlopen(req)
    else:
        parm = urllib.urlencode({'port': config['server']['port'], "host": config['server']['host']})
        req = urllib2.Request(config['url'] + '/api/reg.php', parm)
        res = urllib2.urlopen(req)
    s = str(res.read())
    if s.find('601'):
        pass
    elif s.find('602'):
        base.err_log(602, '注册失败')
    else:
        base.err_log(500, '注册时获得未知的数据:' + s)


if __name__ == '__main__':
    reg()
