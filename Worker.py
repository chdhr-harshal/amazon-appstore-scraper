# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import argparse
from utils.CurlReq import request
from utils.Utils import Utils
from parser import app_info_parser
from parser import app_review_parser

class Worker:

    def __init__(self):
        """
        Class Constructor
        """

    def get_arguments_parser(self):
        """
        Creates parsing object using argparse module
        """

        parser = argparse.ArgumentParser(description='Scraper / Worker layer \
                                                    of the Amazon Appstore crawler')

        parser.add_argument('--asin',
                            required=True,
                            type=str,
                            help='ASIN of the app')

        parser.add_argument('-title',
                            action='store_true',
                            help='Get title of the app')

        parser.add_argument('-developer',
                            action='store_true',
                            help='Get developer of the app')
        
        parser.add_argument('-developer-url',
                            action='store_true',
                            help='Get developer URL of the app')

        parser.add_argument('-developer-info',
                            action='store_true',
                            help='Get developer info. of the app')

        parser.add_argument('-mas-rating',
                            action='store_true',
                            help='Get content rating of the app')

        parser.add_argument('-price',
                            action='store_true',
                            help='Get price of the app')

        parser.add_argument('-iap',
                            action='store_true',
                            help='In App Purchase flag of the app')

        parser.add_argument('-release-date',
                            action='store_true',
                            help='Release date of the app')

        parser.add_argument('-overall-rank',
                            action='store_true',
                            help='Overall rank of the app')

        parser.add_argument('-version',
                            action='store_true',
                            help='Get current version of the app')

        parser.add_argument('-size',
                            action='store_true',
                            help='Get size of the app')

        parser.add_argument('-min-os-version',
                            action='store_true',
                            help='Get minimum supported os version of the app')

        parser.add_argument('-total-reviews',
                            action='store_true',
                            help='Get total reviews of the app')

        parser.add_argument('-avg-star-rating',
                            action='store_true',
                            help='Get average star rating of the app')

        parser.add_argument('-star-rating-hist',
                            action='store_true',
                            help='Get star rating histogram of the app')

        parser.add_argument('-category-rank',
                            action='store_true',
                            help='Get categorical rank of the app')

        parser.add_argument('-categories',
                            action='store_true',
                            help='Get all categories of the app')

        parser.add_argument('-icon-url',
                            action='store_true',
                            help='Get icon url of the app')

        parser.add_argument('-permissions',
                            action='store_true',
                            help='Get all permissions of the app')

        parser.add_argument('-description',
                            action='store_true',
                            help='Get description of the app')

        parser.add_argument('-similar-apps',
                            action='store_true',
                            help='Get similar apps of the app')

        parser.add_argument('-reviews',
                            action='store_true',
                            help='Get all reviews of the app')

        return parser
