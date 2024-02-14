"""
    Functions to parse string and transorm as colored output of:
    GREEN - SUCCESS
    RED - ERROR
    BLUE - MESSAGE
    YELLOW - WARNING
    MAGENTA - DEBUG
"""

import logging

from colorama import Fore, Style

BASIC_FORMAT = "[%(asctime)s] [%(filename)s:%(lineno)s] %(message)s"
logging.basicConfig(format=BASIC_FORMAT, level=logging.INFO, datefmt="%d.%m.%Y - %H:%M")


class ColoredLogger:
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name

    def create_logger(self):
        """
        Creates a logger
        """
        LOG = logging.getLogger(self.app_name)
        LOG.setLevel(logging.INFO)
        return LOG

    def green(self, message: str):
        """
        Prints Green
        """
        return f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}"

    def red(self, message: str):
        """
        Prints Red
        """
        return f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}"

    def yellow(self, message: str):
        """
        Prints Yellow
        """
        return f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}"

    def cyan(self, message: str):
        """
        Prints Blue
        """
        return f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}"

    def magenta(self, message: str):
        """
        Prints Magenta
        """
        return f"{Fore.MAGENTA}[DEBUG]{Style.RESET_ALL} {message}"
