# !/home/grad3/harshal/py_env/my_env/bin/python2.7

import logging
import random

class Utils:
    """
    This class shares useful codes between bootstrapper and the
    worker layers of the scraper
    """

    @staticmethod
    def get_log_level_from_string(logLevel):
        """
        Returns the proper logging level based
        on the string received.
    
        Positional Arguments:
            - logLevel (str) - Log level as string

        returns the logging level (int) that matches the string received
        """

        if logLevel == 'DEBUG':
            return logging.DEBUG

        elif logLevel == 'WARN':
            return logging.WARN

        elif logLevel == 'ERROR':
            return logging.ERROR

        elif logLevel == 'CRITICAL':
            return logging.CRITICAL

        elif logLevel == 'INFO':
            return logging.INFO

        else:
            return None


    @staticmethod
    def configure_log(args):
        """
        Configures the logger object that is used
        for logging to both CLI output and file
        
        returns : An instance of a logger class
        """
    
        cli_log_verbosity = args['console_log_verbosity']
        file_log_verbosity = args['file_log_verbosity']

        # Console log Level

        cli_log_level = Utils.get_log_level_from_string(cli_log_verbosity)
        file_log_level = Utils.get_log_level_from_string(file_log_verbosity)

        # Creating Logger and Configuring console handler
        logger = logging.getLogger('Bootstrapper')
        logger.setLevel(cli_log_level)
        cli_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - \
                                        %(levelname)s - \
                                        %(message)s')
        cli_handler.setFormatter(formatter)
        logger.addHandler(cli_handler)

        # Check for the need to create a log file
        if args['log_file']:
            file_handler = logging.FileHandler(args['log_file'])
            file_handler.setLevel(file_log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
