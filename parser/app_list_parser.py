# !/home/grad3/harshal/py_env/my_env/bin/python2.7

from bs4 import BeautifulSoup as bs
import re
import string

class parser:
    def __init__(self, html):
        self.html = filter(lambda x: x in string.printable, html)
        self.soup = bs(self.html, "lxml")

    def get_asins(self):
        apps = self.soup.findAll('li', {'class':'s-result-item s-result-card-for-container a-declarative celwidget'})
        asins = [app['data-asin'] for app in apps]
        return asins

    def pagination_next_list_page(self):
        pagination = self.soup.find('a', {'id':'pagnNextLink'})
        if pagination:
            return True
        else:
            return False
