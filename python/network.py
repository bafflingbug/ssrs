import urllib
import urllib2
import socket


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
    res = urllib2.urlopen(url)
    return str(res.read())


def post(url, data, token, host):
    parm = urllib.urlencode({'ssr': data, "token": token, "host": host})
    req = urllib2.Request(url, parm)
    res = urllib2.urlopen(req)
    return str(res.read())


def active(url, token, host):
    parm = urllib.urlencode({"token": token, "host": host})
    req = urllib2.Request(url, parm)
    res = urllib2.urlopen(req)
    return str(res.read())
