# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import logging
import argparse
from utils.CurlReq import request
from utils import Utils

class Bootstrapper:

    def __init__(self):
        """
        Database access parameters
        """
        params = {}
        params['server'] = 'ist-www-mysql-prod.bu.edu'
        params['port'] = '3309'
        params['database'] = 'amazon_appstore'
        params['username'] = 'amazon_appstore'
        params['password'] = 'sP7sw8chuchu'

        self._params = params

    def get_arguments_parser(self):
        """
        Creates argument parser object
        using argparse module
        """
        
        parser = argparse.ArgumentParser(description='Bootstrapping phase of \
                                                     the Amazon Appstore \
                                                     Crawler')
    

        # All arugments start with "-", so, they are all handled as optional
        parser.add_argument('--console-log-verbosity',
                            type=str,
                            choices=['INFO', 'DEBUG', 'WARN',
                                     'ERROR', 'CRITICAL'],
                            help='Log Verbosity Level (default=INFO)',
                            default='INFO')

        parser.add_argument('--file-log-verbosity',
                            type=str,
                            choices=['INFO', 'DEBUG', 'WARN',
                                     'ERROR', 'CRITICAL'],
                            help='Log Verbosity Level (default=ERROR)',
                            default='ERROR')

        parser.add_argument('--log-file',
                            type=str,
                            help='Path of the output log file (default=\
                                    console-only logging)')

        parser.add_argument('--use-proxy',
                            type=bool,
                            help='Boolean indicating proxy usage',
                            default=False)

        return parser

    def start_bootstrapper(self):
        """
        Main Method 
        """
        
        # Arguments Parsing
        args_parser = self.get_arguments_parser()
        self._args = vars(args_parser.parse_args())

        # Log Handler Configuring
        self._logger = Utils.configure_log(self._args)


# Starting Point
if __name__ == "__main__":
        bootstrapper = Bootstrapper()
        bootstrapper.start_bootstrapper()
        
