import logging
import os

from helpers import constants

# Configure the root logger
BASIC_FORMAT = "[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=BASIC_FORMAT, level=logging.INFO, datefmt="%d.%m.%Y - %H:%M")

# Create a file handler to save logs to a file
file_handler = logging.FileHandler(
    f"{os.getcwd()}/logging/wbmbot-v2_{constants.today}.log"
)
file_handler.setLevel(logging.INFO)  # Set the desired log level for file output
# Create a formatter to format log messages
formatter = logging.Formatter(
    "[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s"
)
# Set the formatter for both handlers
file_handler.setFormatter(formatter)
# Get the root logger and add both handlers to it
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)
