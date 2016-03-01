#!/home/grad3/harshal/py_env/my_env/bin/python2.7

import argparse
from utils.CurlReq import request
from utils.Utils import Utils
from amazon_parser import app_info_parser
from amazon_parser import app_review_parser
from crawler.app_info_crawler import crawler as info_crawler
from crawler.app_review_crawler import crawler as review_crawler

class Worker:

    def __init__(self):
        """
        Class Constructor
        """
        self.asin = None
        self.args = None
        self.optional_info_args = None
    
        self.crawl_app_info = True
        self.crawl_app_reviews = False

    def get_arguments_parser(self):
        """
        Creates parsing object using argparse module
        """

        parser = argparse.ArgumentParser(description='Scraper / Worker layer \
                                                    of the Amazon Appstore crawler')

        parser.add_argument('asin',
                            type=str,
                            help='ASIN of the app')

        parser.add_argument('--title',
                            action='store_true',
                            help='Get title of the app')

        parser.add_argument('--developer',
                            action='store_true',
                            help='Get developer of the app')
        
        parser.add_argument('--developer-url',
                            action='store_true',
                            help='Get developer URL of the app')

        parser.add_argument('--developer-info',
                            action='store_true',
                            help='Get developer info. of the app')

        parser.add_argument('--content-rating',
                            action='store_true',
                            help='Get content rating of the app')

        parser.add_argument('--price',
                            action='store_true',
                            help='Get price of the app')

        parser.add_argument('--iap',
                            action='store_true',
                            help='In App Purchase flag of the app')

        parser.add_argument('--release-date',
                            action='store_true',
                            help='Release date of the app')

        parser.add_argument('--overall-rank',
                            action='store_true',
                            help='Overall rank of the app')

        parser.add_argument('--version',
                            action='store_true',
                            help='Get current version of the app')

        parser.add_argument('--size',
                            action='store_true',
                            help='Get size of the app')

        parser.add_argument('--min-os-version',
                            action='store_true',
                            help='Get minimum supported os version of the app')

        parser.add_argument('--total-reviews',
                            action='store_true',
                            help='Get total reviews of the app')

        parser.add_argument('--avg-star-rating',
                            action='store_true',
                            help='Get average star rating of the app')

        parser.add_argument('--star-rating-hist',
                            action='store_true',
                            help='Get star rating histogram of the app')

        parser.add_argument('--category-rank',
                            action='store_true',
                            help='Get categorical rank of the app')

        parser.add_argument('--categories',
                            action='store_true',
                            help='Get all categories of the app')

        parser.add_argument('--icon-url',
                            action='store_true',
                            help='Get icon url of the app')

        parser.add_argument('--permissions',
                            action='store_true',
                            help='Get all permissions of the app')

        parser.add_argument('--description',
                            action='store_true',
                            help='Get description of the app')

        parser.add_argument('--similar-apps',
                            action='store_true',
                            help='Get similar apps of the app')

        parser.add_argument('--reviews',
                            action='store_true',
                            help='Get all reviews of the app')
        
        parser.add_argument('--app-info',
                            action='store_true',
                            help='Get all info of the app')

        parser.add_argument('--use-proxy',
                            action='store_true',
                            help='Use proxy')

        return parser

    def scrape(self):
        info_cr = info_crawler(self.asin, self.args.use_proxy)
        review_cr = review_crawler(self.asin, self.args.use_proxy)

        app_info = info_cr.crawl_info_page()
        if len(self.optional_info_args.keys()) == 0 and self.crawl_app_info:
            for item in app_info:
                print "{0} : {1}\n".format(item, app_info[item])
        else:
            for item in self.optional_info_args:
                print "{0} : {1}\n".format(item, app_info[item])

        if self.crawl_app_reviews == True:
            reviews = review_cr.crawl_reviews()
            
            for review in reviews:
                print review
            

    def start_worker(self):
        args_parser = self.get_arguments_parser()
        args = args_parser.parse_args()
        self.asin = args.asin
        self.args = args
        optional_args = dict(filter(lambda x : x[1] == True, vars(args).items()))

        if 'use_proxy' in optional_args.keys():
            del optional_args['use_proxy']

        if 'reviews' in optional_args.keys():
            del optional_args['reviews']
            self.crawl_app_reviews = True
            self.crawl_app_info = False

        self.optional_info_args = optional_args

        self.scrape()
        

if __name__ == "__main__":
    worker = Worker()
    worker.start_worker()
