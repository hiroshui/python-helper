"""
This file contains the main entry point for the email autoresponder application.

The application reads email messages from an Outlook inbox, responds to them with a predefined message,
and saves the content of unread messages to a CSV file. The application uses the EmailProcessor class
from the email_processor module to handle email processing.

The file also sets up a logger to record application events to a log file and the console.
"""

import logging

from models.email_processor import EmailProcessor

# Create a logger and set the logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and set the logging level
file_handler = logging.FileHandler('automailer.log')
file_handler.setLevel(logging.INFO)

# Create a stream handler and set the logging level
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == '__main__':
    config_file = 'config.ini'
    processor = EmailProcessor(config_file=config_file, logger=logger)
    processor.run()