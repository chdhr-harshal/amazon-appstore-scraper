# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import subprocess
import random
import urllib
from fake_useragent import UserAgent

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
        if self.proxy == False:
            # Make request without any proxy
            cmd = """curl -i """
        else:
            ratio = 1.0 * len(self.http_proxy_list) / len(self.socks_proxy_list)
            key = random.random() 
            if key < ratio:
                # Make request through http proxy
                rand = random.randint(0, len(self.http_proxy_list)-1)
                proxy = self.http_proxy_list[rand]
                cmd = """curl -i --proxy https://{0} """.format(proxy)
            else:
                # Make request through socks proxy
                rand = random.randint(0, len(self.socks_proxy_list)-1)
                proxy = self.socks_proxy_list[rand]
                cmd = """curl -i --socks5-hostname {0} """.format(proxy)

            # Authentication and timeout parameters
            cmd += "--proxy-user {0}:{1} ".format(username, password)
        
        # Parts of command common for both proxy and no proxy requests
        cmd += "--connect-timeout 5 "
        cmd += "--retry 1 " 
        # Data for POST request 
        if data:
            cmd += """--data {0} """.format(urllib.urlencode(data))
        
        cmd += """--user-agent {0} """.format(self.ua.random)
        cmd += url

        args = cmd.split()
        process = subprocess.Popen(args, shell=False,   \
                                stdout=subprocess.PIPE, \
                                stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        return (stdout, stderr)

    def read_http_proxy_list(self):
        with open('/research/analytics/proxylist/http_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.http_proxy_list = [proxy.strip() for proxy in proxies]
 
    def read_socks_proxy_list(self):
        with open('/research/analytics/proxylist/socks5_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.socks_proxy_list = [proxy.strip() for proxy in proxies]

