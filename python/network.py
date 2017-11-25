import urllib
import urllib2


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
