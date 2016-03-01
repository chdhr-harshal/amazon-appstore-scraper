#!/home/grad3/harshal/py_env/my_env/bin/python2.7

# Append root directory to system path
import sys
sys.path.append('..')

from utils.CurlReq import request
from amazon_parser.app_info_parser import parser
import argparse

class crawler:

    def __init__(self, asin, use_proxy=False):
        self.asin = asin
        self.use_proxy = use_proxy

        self.app_url = 'http://www.amazon.com/dp/{0}'
        self.r = request(self.use_proxy)

        self.app_info = None
        self.pr = None

    def check_result(self, result):
        status_code = result[0]
        html = result[1]
    
        # Status code in 2xx series
        if status_code/100 == 2:
            if 'Write a customer review' in html:
                self.pr = parser(html)
                return True
            else:
                return False
        # Status code in 4xx series
        elif status_code/100 == 4:
            return False
        # Status code in 3xx series
        else:
            return False

    def crawl_info_page(self):
        url = self.app_url.format(self.asin)
        result = self.r.fetch(url)

        if self.check_result(result):
            self.app_info = self.pr.get_app_info()
        else:
            pass

        return self.app_info

def get_argument_parser():
    parser = argparse.ArgumentParser(description='App info crawler \
                                                 for provided ASIN')

    parser.add_argument('asin',
                        type=str,
                        help='ASIN of app')

    parser.add_argument('--use-proxy',
                        action='store_true',
                        help='Use proxy')

    return parser

def main():
    args_parser = get_argument_parser()
    args = args_parser.parse_args()
    cr = crawler(args.asin, args.use_proxy)
    app_info = cr.crawl_info_page()
    return app_info

if __name__ == "__main__":
    main()
