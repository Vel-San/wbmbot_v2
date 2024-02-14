import json
import os

from logger import wbm_logger
from utility import interaction


# Function to check for the existence of the config file and load it
def load_wbm_config(file_name: str):
    """
    Loads the wbm config, or create it if not found

    Parameters:
        file_name (str): The path to the file.
    """

    if os.path.isfile(file_name):
        wbm_logger.logging.info("Loading WBM config..")
        with open(file_name, "r") as config_file:
            try:
                user_config = json.load(config_file)
                return user_config
            except json.JSONDecodeError as e:
                wbm_logger.logging.error(f"Error parsing WBM config file! ({e})")
            except TypeError as e:
                wbm_logger.logging.error(f"Error parsing WBM config file! ({e})")
    else:
        wbm_logger.logging.warning("No WBM config file found, starting setup..")
        # Setup WBM config from the User
        interaction.setup_wbm_config()
        wbm_logger.logging.info("Loading WBM config..")
        with open(file_name, "r") as config_file:
            try:
                user_config = json.load(config_file)
                return user_config
            except json.JSONDecodeError as e:
                wbm_logger.logging.error(f"Error parsing WBM config file! ({e})")
            except TypeError as e:
                wbm_logger.logging.error(f"Error parsing WBM config file! ({e})")


def initialize_application_logger(log_file: str):
    """
    Checks if a file exists at the specified path and creates it if it doesn't.

    Parameters:
        file_path (str): The path to the file.
    """

    # Check if the log file exists
    if not os.path.isfile(log_file):
        # If the log file does not exist, create it by opening in append mode and immediately closing it
        with open(log_file, "a") as file:
            pass


def write_log_file(log_file: str, entry: str):
    """Write an entry to the log file."""
    with open(log_file, "a") as myfile:
        myfile.write(entry)


def read_log_file(log_file: str):
    """Read and return the content of the log file."""
    with open(log_file, "r") as myfile:
        return myfile.read()
