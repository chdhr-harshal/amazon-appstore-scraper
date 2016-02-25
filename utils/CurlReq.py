# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import subprocess
import random
import urllib
from fake_useragent import UserAgent
import pycurl
import cStringIO

# Read proxy credentials
f = open('/research/analytics/proxylist/proxy_credentials','r')
rows = f.readlines()
f.close()

# Or you can manually specify it right below
username = rows[0].strip().split(':')[1]
password = rows[1].strip().split(':')[1]

class request():
    def __init__(self, proxy=False):
        
        self.http_proxy_list = []
        self.socks_proxy_list = []

        self.read_http_proxy_list()
        self.read_socks_proxy_list()
        
        self.ua = UserAgent()
        self.proxy = proxy


    def fetch(self, url, data=None):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)

        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        
        c.setopt(pycurl.HEADERFUNCTION, hdr.write)
        c.setopt(pycurl.WRITEFUNCTION, buff.write)

        c.setopt(pycurl.TIMEOUT, 10)
        c.setopt(pycurl.USERAGENT, self.ua.random)

        if data:
            c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
        
        if self.proxy == True:
            c.setopt(pycurl.PROXYUSERPWD, "{0}:{1}".format(username, password))

            ratio = 1.0 * len(self.http_proxy_list) / len(self.socks_proxy_list)
            key = random.random()
            if key < ratio:
                # Make request through http proxy
                rand = random.randint(0, len(self.http_proxy_list)-1)
                proxy = self.http_proxy_list[rand]
                c.setopt(pycurl.PROXY, "https://{0}".format(proxy))             
            else:
                # Make request through socks proxy
                rand = random.randint(0, len(self.socks_proxy_list)-1)
                proxy = self.socks_proxy_list[rand]
                c.setopt(pycurl.PROXY, proxy.split(':')[0])
                c.setopt(pycurl.PROXYPORT, int(proxy.split(':')[1]))
                c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
        try:
            c.perform()
        except pycurl.error, e:
            # If it was a 'User rejected or Connection refused error
            # remove proxy from the list
            if e[0] == 7:
                try:
                    self.socks_proxy_list.remove(proxy)
                except:
                    self.http_proxy_list.remove(proxy)
            return e

        return (c.getinfo(pycurl.HTTP_CODE), buff.getvalue())

    def read_http_proxy_list(self):
        with open('/research/analytics/proxylist/http_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.http_proxy_list = [proxy.strip() for proxy in proxies]
 
    def read_socks_proxy_list(self):
        with open('/research/analytics/proxylist/socks5_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.socks_proxy_list = [proxy.strip() for proxy in proxies]

