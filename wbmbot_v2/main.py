import argparse
import os

from chromeDriver import chrome_driver_configurator as cdc
from handlers import user
from helpers import constants, webDriverOperations
from logger import wbm_logger
from utility import io_operations

__appname__ = os.path.splitext(os.path.basename(__file__))[0]


def parse_args():
    """
    Parse the command line arguments
    """

    parser = argparse.ArgumentParser(
        description="A Selenium-based bot that scrapes 'WBM Angebote' page and auto applies on appartments based on user exclusion filters",
        usage="%(prog)s " "[-i] " "[-H] " "[-t]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--interval",
        dest="interval",
        default=3,
        required=False,
        help="Set the time interval in 'minutes' to check for new flats (refresh) on wbm.de. [default: 3 minutes]",
    )
    parser.add_argument(
        "-H",
        "--headless_off",
        dest="headless_off",
        action="store_false",
        default=True,
        required=False,
        help="If set, turn 'OFF' headless run. The bot will run directly in the browser.",
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="test",
        action="store_true",
        default=False,
        required=False,
        help="If set, run test-run on the test data. This does not actually connect to wbm.de.",
    )

    return parser.parse_args()


# * Script Starts Here
if __name__ == "__main__":
    args = parse_args()

    color_me = wbm_logger.ColoredLogger(__appname__)
    LOG = color_me.create_logger()

    # Create ChromeDriver
    LOG.info(color_me.cyan("Initializing Script"))
    chrome_driver_instance = cdc.ChromeDriverConfigurator(args.headless_off, args.test)
    web_driver = chrome_driver_instance.get_driver()

    # Create WBM Config
    wbm_config = io_operations.load_wbm_config(constants.wbm_config_name)
    # Create User Profile
    user_profile = user.User(wbm_config)
    # Create Logger file
    io_operations.initialize_application_logger(constants.log_file_path)
    # Get URL
    start_url = constants.wbm_url if not args.test else constants.test_wbm_url

    ###### Start the magic ######
    current_page = 1
    previous_page = 1
    page_changed = False
    LOG.info(color_me.cyan(f"Connecting to '{start_url}'"))

    webDriverOperations.process_flats(
        web_driver,
        user_profile,
        start_url,
        current_page,
        previous_page,
        page_changed,
        args.interval,
    )

# driver.quit()
