# !/home/grad3/harshal/py_env/my_env/bin/python2.7

from bs4 import BeautifulSoup as bs
import re
import string
from math import ceil

class parser:
    def __init__(self, html):
        self.html = filter(lambda x: x in string.printable, html)
        self.soup = bs(self.html, "lxml")

    def pagination_next_list_page(self):
        pagination = self.soup.find('a', {'id':'pagnNextLink'})
        if pagination:
            return True
        else:
            return False

    def get_total_pages(self):
        total_items = self.soup.find('h2', {'id':'s-result-count'}).text
        total_items = float(total_items.split(' ')[2].replace(',',''))
        total_pages = int(ceil(total_items/60))
        return total_pages
    
    def get_asins(self):
        apps = self.soup.findAll('li', {'class':'s-result-item s-result-card-for-container a-declarative celwidget'})
        asins = [app['data-asin'] for app in apps]

        return asins

