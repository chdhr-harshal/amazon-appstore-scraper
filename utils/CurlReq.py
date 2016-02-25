# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import subprocess
import random
import urllib
from fake_useragent import UserAgent
import pycurl
import cStringIO

class request():
    def __init__(self, use_proxy=False):
        
        self.http_proxy_list = []
        self.socks_proxy_list = []

        if use_proxy:
            # Read proxy credentials
            f = open('/research/analytics/proxylist/proxy_credentials','r')
            rows = f.readlines()
            f.close()
            
            self.username = rows[0].strip().split(':')[1]
            self.password = rows[1].strip().split(':')[1]

            self.read_http_proxy_list()
            self.read_socks_proxy_list()
        
        self.ua = UserAgent()
        self.use_proxy = use_proxy
        self.last_sent_proxy_type = None
        self.last_sent_proxy = None

    def set_proxy(self, curl):
        ratio = 1.0 * len(self.http_proxy_list) / len(self.socks_proxy_list)
        key = random.random()

        if key < ratio:
            # Set http proxy
            rand = random.randint(0, len(self.http_proxy_list)-1)
            proxy = self.http_proxy_list[rand]
            curl.setopt(pycurl.PROXY, proxy.split(':')[0])
            curl.setopt(pycurl.PROXYPORT, int(proxy.split(':')[1]))
            curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)

            self.last_sent_proxy_type = 'HTTP'
            self.last_sent_proxy = proxy
        else:
            # Set socks proxy
            rand = random.randint(0, len(self.socks_proxy_list)-1)
            proxy = self.socks_proxy_list[rand]
            curl.setopt(pycurl.PROXY, proxy.split(':')[0])
            curl.setopt(pycurl.PROXYPORT, int(proxy.split(':')[1]))
            curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

            self.last_sent_proxy_type = 'SOCKS'
            self.last_sent_proxy = proxy
        return curl

    def remove_proxy(self):
        if self.last_sent_proxy_type == 'HTTP':
            self.http_proxy_list.remove(self.last_sent_proxy)
        else:
            self.socks_proxy_list.remove(self.last_sent_proxy)

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
        
        if self.use_proxy:
            c.setopt(pycurl.PROXYUSERPWD, "{0}:{1}".format(self.username, self.password))
            c = self.set_proxy(c)

        while True:
            try:
                c.perform()
            except pycurl.error, e:
                self.remove_proxy()
                c = self.set_proxy(c)
            else:
                return (c.getinfo(pycurl.HTTP_CODE), buff.getvalue())

    def read_http_proxy_list(self):
        with open('/research/analytics/proxylist/http_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.http_proxy_list = [proxy.strip() for proxy in proxies]
 
    def read_socks_proxy_list(self):
        with open('/research/analytics/proxylist/socks5_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.socks_proxy_list = [proxy.strip() for proxy in proxies]

