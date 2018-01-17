#!/usr/bin/python
# -*- coding: utf-8 -*-
from proxy.py3 import PY3
import proxy.base as base

if PY3:
    from urllib import request, parse
else:
    import urllib
    import urllib2


def reg():
    config = base.get_config()
    if PY3:
        data = parse.urlencode(
            {'port': config['server']['port'], "host": config['server']['host'], 'token': config['token']}).encode(
            'utf-8')
        req = request.Request(config['url'] + '/api/reg.php', data=data)
        res = request.urlopen(req)
    else:
        parm = urllib.urlencode(
            {'port': config['server']['port'], "host": config['server']['host'], 'token': config['token']})
        req = urllib2.Request(config['url'] + '/api/reg.php', parm)
        res = urllib2.urlopen(req)
    s = base.str_auto(res.read())
    print(s)
    if s.find('601') != -1:
        pass
    elif s.find('602') != -1:
        base.err_log(602, '注册失败')
    elif s.find('401') != -1:
        base.err_log(401, '注册时token错误')
    else:
        base.err_log(500, '注册时获得未知的数据:' + s)


if __name__ == '__main__':
    reg()
