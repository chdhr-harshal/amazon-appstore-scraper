# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import subprocess
import random

# Read proxy credentials
f = open('/research/analytics/proxylist/proxy_credentials','r')
rows = f.readlines()
f.close()

# Or you can manually specify it right below
username = rows[0].strip().split(':')[1]
password = rows[1].strip().split(':')[1]

class proxy():
    def __init__(self):
        
        self.http_proxy_list = []
        self.socks_proxy_list = []

        self.read_http_proxy_list()
        self.read_socks_proxy_list()

    def __call__(self, url, data=None):
        
        ratio = 1.0 * len(self.http_proxy_list) / len(self.socks_proxy_list)
        key = random.random()
        
        if key < ratio:
            # Make request through http proxy

            rand = random.randint(0, len(self.http_proxy_list)-1)
            proxy = self.http_proxy_list[rand]

            cmd = """curl --proxy https://{0} --proxy-user {1}:{2} --max-time 5 """.format(proxy, username, password)
            cmd += url

            args = cmd.split()
            process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
        else:
            # Make request through socks proxy
        
            rand = random.randint(0, len(self.socks_proxy_list)-1)
            proxy = self.socks_proxy_list[rand]

            cmd = """curl --socks5-hostname {0} --proxy-user {1}:{2} --max-time 5 """.format(proxy, username, password)
            cmd += url

            args = cmd.split()
            process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

        if stdout:
            return stdout
        else:
            return None

    def read_http_proxy_list(self):
        with open('/research/analytics/proxylist/http_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.http_proxy_list = [proxy.strip() for proxy in proxies]
 
    def read_socks_proxy_list(self):
        with open('/research/analytics/proxylist/socks5_proxylist/proxylist') as f:
            proxies = f.readlines()

        self.socks_proxy_list = [proxy.strip() for proxy in proxies]
