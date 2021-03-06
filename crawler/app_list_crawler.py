#!/home/grad3/harshal/py_env/my_env/bin/python2.7

# Append root directory to system path
import sys
sys.path.append('..')

from utils.CurlReq import request
from amazon_parser.app_list_parser import parser
import argparse

class crawler:
    
    def __init__(self, node_index, use_proxy=False):
        self.node_index = node_index
        self.next_page_exists = True
        self.use_proxy = use_proxy

        self.app_list_url = 'http://www.amazon.com/s/rh=n:{0}&page={1}&fap=1'
        self.r = request(self.use_proxy)

        self.asin_list = []
        self.pr = None

        self.current_page = 1
        self.max_pages = 400

    def check_result(self, result):
        status_code = result[0]
        html = result[1]

        # Status code in 2xx series
        if status_code/100 == 2:
            self.pr = parser(html)
            asins = self.pr.get_asins()
            if len(asins) > 0:
                self.next_page_exists = self.pr.pagination_next_list_page()
                return True
            else:
                return False
        # Status code in 4xx series
        elif status_code/100 == 4:
            self.next_page_exists = False
            return False
        # Status code in 3xx series
        else:
            self.next_page_exists = False
            return False
            

    def crawl_list(self):
        while self.next_page_exists:
            # Amazon only shows first 400 pages of results
            if self.current_page > self.max_pages:
                break

            url = self.app_list_url.format(self.node_index, self.current_page)
            result = self.r.fetch(url)

            if self.check_result(result):
                asins = self.pr.get_asins()
                self.asin_list += asins
                print "Fetched {0} apps from url : {1}".format(len(asins), url)
                self.current_page += 1
            else:
                continue
        return self.asin_list

def get_argument_parser():
    parser = argparse.ArgumentParser(description='App list parser')

    parser.add_argument('node',
                        type=str,
                        help='Amazon app list node id')

    parser.add_argument('--use-proxy',
                        action='store_true',
                        help='Use proxy')

    return parser

def main():
    args_parser = get_argument_parser()
    args = args_parser.parse_args()
    cr = crawler(args.node, args.use_proxy)
    asins = cr.crawl_list()

if __name__ == "__main__":
    main()
