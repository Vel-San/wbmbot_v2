import json
import os
import re

from helpers import constants
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


def write_log_file(log_file: str, email: str, flat_obj):
    """
    Write a nested dictionary log entry to the log file.

    Parameters:
        log_file (str): The path to the JSON log file.
        email (str): The email associated with the log entry.
        flat_obj (object): An object containing information about the flat.

    Returns:
        None
    """

    # Read existing log entries
    try:
        with open(log_file, "r") as json_file:
            existing_log = json.load(json_file)
    except FileNotFoundError:
        existing_log = {}
    except json.decoder.JSONDecodeError:
        existing_log = {}

    # Check if email already exists in the log
    if email in existing_log:
        # Check if the entry with the same hash exists
        if flat_obj.hash not in existing_log[email]:
            existing_log[email][flat_obj.hash] = {
                "date": constants.today.isoformat(),
                "title": flat_obj.title,
                "street": flat_obj.street,
                "zip_code": flat_obj.zip_code,
                "rent": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.total_rent),
                "size": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.size),
                "rooms": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.rooms),
                "wbs?": flat_obj.wbs,
            }
    else:
        # If email doesn't exist, add a new entry
        existing_log[email] = {
            flat_obj.hash: {
                "date": constants.today.isoformat(),
                "title": flat_obj.title,
                "date": constants.today.isoformat(),
                "title": flat_obj.title,
                "street": flat_obj.street,
                "zip_code": flat_obj.zip_code,
                "rent": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.total_rent),
                "size": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.size),
                "rooms": re.sub(r"(\D)(\d)", r"\1 \2", flat_obj.rooms),
                "wbs?": flat_obj.wbs,
            }
        }

    # Write the updated log back to the file
    with open(log_file, "w") as json_file:
        json.dump(existing_log, json_file, indent=4, ensure_ascii=False)


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


def check_flat_already_applied(log_file: str, email: str, flat_obj):
    """
    Check if an application for the flat has already been sent.

    Parameters:
        log_file (str): The path to the JSON log file.
        flat_obj (object): An object containing information about the flat.
        email (str): The email associated with the log entry.

    Returns:
        bool: True if an application has already been sent, False otherwise.
    """

    try:
        with open(log_file, "r") as json_file:
            log = json.load(json_file)
    except FileNotFoundError:
        return False
    except json.decoder.JSONDecodeError:
        return False

    email = email.strip()
    if email in log:
        for flat_hash, flat_data in log[email].items():
            if flat_hash == flat_obj.hash:
                return True
    return False
