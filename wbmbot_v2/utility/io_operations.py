import json
import os

from logger import wbm_logger
from utility import interaction

__appname__ = os.path.splitext(os.path.basename(__file__))[0]
color_me = wbm_logger.ColoredLogger(__appname__)
LOG = color_me.create_logger()


# Function to check for the existence of the config file and load it
def load_wbm_config(file_name: str):
    """
    Loads the wbm config, or create it if not found

    Parameters:
        file_name (str): The path to the file.
    """

    if os.path.isfile(file_name):
        LOG.info(color_me.cyan("Loading WBM config"))
        with open(file_name, "r") as config_file:
            try:
                user_config = json.load(config_file)
                return user_config
            except json.JSONDecodeError as e:
                LOG.error(color_me.red(f"Failed to parse WBM config file! ({e})"))
            except TypeError as e:
                LOG.error(color_me.red(f"Failed to parse WBM config file! ({e})"))
    else:
        LOG.warning(color_me.yellow("No WBM config file found, starting setup"))
        # Setup WBM config from the User
        interaction.setup_wbm_config()
        LOG.info(color_me.cyan("Loading WBM config"))
        with open(file_name, "r") as config_file:
            try:
                user_config = json.load(config_file)
                return user_config
            except json.JSONDecodeError as e:
                LOG.error(color_me.red(f"Failed to parse WBM config file! ({e})"))
            except TypeError as e:
                LOG.error(color_me.red(f"Failed to parse WBM config file! ({e})"))


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


def create_directory_if_not_exists(directory_path: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory_path (str): The path of the directory to be created.

    Returns:
        None
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
    except OSError as e:
        LOG.error(color_me.red(f"Error to create directory ({directory_path}): {e}"))
