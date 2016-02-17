# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import subprocess
import random
import urllib

# Read proxy credentials
f = open('/research/analytics/proxylist/proxy_credentials','r')
rows = f.readlines()
f.close()

# Or you can manually specify it right below
username = rows[0].strip().split(':')[1]
password = rows[1].strip().split(':')[1]

class request():
    def __init__(self):
        
        self.http_proxy_list = []
        self.socks_proxy_list = []

        self.read_http_proxy_list()
        self.read_socks_proxy_list()

    def fetch(self, url, data=None):
        ratio = 1.0 * len(self.http_proxy_list) / len(self.socks_proxy_list)
        key = random.random() 
        if key < ratio:
            # Make request through http proxy
            rand = random.randint(0, len(self.http_proxy_list)-1)
            proxy = self.http_proxy_list[rand]
            cmd = """curl --proxy https://{0} """.format(proxy)
        else:
            # Make request through socks proxy
            rand = random.randint(0, len(self.socks_proxy_list)-1)
            proxy = self.socks_proxy_list[rand]
            cmd = """curl --socks5-hostname {0} """.format(proxy)

        # Authentication and timeout parameters
        cmd += "--proxy-user {0}:{1} ".format(username, password)
        cmd += "--connect-timeout 5 "
   
        # Data for POST request 
        if data:
            data = urllib.urlencode(data)
            cmd += """--data {0} """.format(data)
        
        user_agent = self.get_user_agent()
        cmd += """--user-agent {0} """.format(user_agent)
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

    def get_user_agent(self):
        # Randomize user-agent for each proxy browser instance
        platform = random.choice(['Macintosh', 'Windows', 'X11'])
        if platform == 'Macintosh':
            os = random.choice(['68K','PPC'])
        elif platform == 'Windows':
            os = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 
                                'Windows NT 5.1', 'Windows NT     5.2', 'Windows NT 6.0', 
                                'Windows NT 6.1', 'Windows NT 6.2', 'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
        elif platform == 'X11':
            os = random.choice(['Linux i686', 'Linux x86_64'])

        browser = 'firefox'
        year = str(random.randint(2000, 2015))
        month = random.randint(1, 12) 
        if month < 10: 
            month = '0' + str(month)
        else:
            month = str(month)
        day = random.randint(1, 30) 
        if day < 10: 
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day 
        version = random.choice(['7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0'])

        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version

