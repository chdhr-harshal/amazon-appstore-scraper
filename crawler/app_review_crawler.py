# !/home/grad3/harshal/py_env/my_env/bin/python2.7

# Append root directory to sytem path
import sys
sys.path.append('..')

from utils.CurlReq import request
from amazon_parser.app_review_parser import parser

class crawler:

    def __init__(self, asin, use_proxy):
        self.asin = asin
        self.next_page_exists = True
        self.use_proxy = use_proxy

        self.app_review_url = 'http://www.amazon.com/product-reviews/{0}/ref=cm_cr_pr_show_all?ie=UTF8&pageSize=50&sortBy=recent&pageNumber={1}'
        self.r = request(self.use_proxy)

        self.reviews = []
        self.pr = None

        self.current_page = 1

    def check_result(self, result):
        status_code = result[0]
        html = result[1]
        
        # Status code in 2xx series
        if status_code/100 == 2:
            if 'Was this review helpful to you?' in html:
                self.pr = parser(html)
                self.next_page_exists = self.pr.pagination_next_review_page()
                return True
            else:
                return False        
        # Status code in 4xx series
        elif status_code/100 == 4:
            return False
        # Status code in 3xx series
        else:
            return False


    def crawl_reviews(self):
        while self.next_page_exists:
            url = self.app_review_url.format(self.asin, self.current_page)
            result = self.r.fetch(url)

            if self.check_result(result):
                reviews = self.pr.get_reviews()
                self.reviews += reviews
                print "Fetched {0} reviews from url : {1}".format(len(reviews), url)
                self.current_page += 1
            else:
                continue
        return self.reviews
