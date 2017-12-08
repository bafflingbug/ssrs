import socket
from py3 import py3

if py3:
    from urllib import request, parse
else:
    import urllib
    import urllib2


def portopen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        print('%d is open' % port)
        return True
    except:
        print('%d is down' % port)
        return False


def getgroup(url):
    if py3:
        res = request.urlopen(url)
    else:
        res = urllib2.urlopen(url)
    return str(res.read())


def post(url, data, token, host):
    if py3:
        data = parse.urlencode({'ssr': data, "token": token, "host": host}).encode('utf-8')
        req = request.Request(url, data=data)
        res = request.urlopen(req)
    else:
        parm = urllib.urlencode({'ssr': data, "token": token, "host": host})
        req = urllib2.Request(url, parm)
        res = urllib2.urlopen(req)
    return str(res.read())


def active(url, token, host):
    if py3:
        data = parse.urlencode({"token": token, "host": host}).encode('utf-8')
        req = request.Request(url, data=data)
        res = request.urlopen(req)
    else:
        parm = urllib.urlencode({"token": token, "host": host})
        req = urllib2.Request(url, parm)
        res = urllib2.urlopen(req)
    return str(res.read())
