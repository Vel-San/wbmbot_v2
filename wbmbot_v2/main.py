import argparse
import os.path
import time

import yaml
from chromeDriver import chrome_driver_configurator as cdc
from handlers import flat
from helpers import constants
from logger import wbm_logger
from selenium.webdriver.common.by import By


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
        default=5,
        required=False,
        help="Set the time interval in 'minutes' to check for new flats (refresh) on wbm.de. [default: 5 minutes]",
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

    # Create ChromeDriver
    wbm_logger.logging.info("Initializing Script")
    chrome_driver_instance = cdc.ChromeDriverConfigurator(args.headless_off, args.test)
    driver = chrome_driver_instance.get_driver()

flats = []
id = 0
curr_page_num = 1
page_changed = False
TEST = args.test


class User:
    def __init__(self, config):
        self.first_name = config["first_name"]
        self.last_name = config["last_name"]
        self.street = config["street"]
        self.zip_code = config["zip_code"]
        self.city = config["city"]
        self.email = config["email"].split(",")
        self.phone = config["phone"]
        self.wbs = True if "yes" in config["wbs"] else False
        self.wbs_date = config["wbs_date"].replace("/", "")
        self.wbs_rooms = config["wbs_rooms"]
        self.filter = config["filter"].split(",")

        if "100" in config["wbs_num"]:
            self.wbs_num = "WBS 100"
        elif "140" in config["wbs_num"]:
            self.wbs_num = "WBS 140"
        elif "160" in config["wbs_num"]:
            self.wbs_num = "WBS 160"
        elif "180" in config["wbs_num"]:
            self.wbs_num = "WBS 180"
        else:
            self.wbs_num = ""


def setup():
    data = {}
    data["first_name"] = input("Please input your first name and confirm with enter: ")
    data["last_name"] = input("Please input your last name and confirm with enter: ")
    email, email_ls, c = "", "", 1
    while "exit" not in email:
        email = input(
            f"Please input email adress {c} and confirm with enter, type 'exit' to exit: "
        )
        email_ls += email.lower()
        email_ls += ","
        c += 1
    data["email"] = email_ls.replace(",exit,", "")
    data["street"] = input(
        "Please input your street and confirm with enter or leave empty and skip with enter: "
    )
    data["zip_code"] = input(
        "Please input your zip_code and confirm with enter or leave empty and skip with enter: "
    )
    data["city"] = input(
        "Please input your city and confirm with enter or leave empty and skip with enter: "
    )
    data["phone"] = input(
        "Please input your phone number and confirm with enter or leave empty and skip with enter: "
    )
    data["wbs"] = input(
        "Do you have a WBS (Wohnberechtigungsschein)?\nPlease type yes / no: "
    )
    if "yes" in data["wbs"]:
        data["wbs_date"] = input(
            "Until when will the WBS be valid?\nPlease enter the date in format month/day/year: "
        )
        data["wbs_num"] = input(
            "What WBS number (Einkommensgrenze nach Einkommensbescheinigung § 9) does your WBS show?\nPlease enter WBS 100 / WBS 140 / WBS 160 / WBS 180: "
        )
        data["wbs_rooms"] = input(
            "For how many rooms is your WBS valid?\nPlease enter a number: "
        )
    else:
        data["wbs_date"] = ""
        data["wbs_num"] = ""
        data["wbs_rooms"] = ""
    if "yes" in input(
        "Do you want to enter keywords to exclude specific flats from the search results?\nPlease type yes / no: "
    ):
        keyword, filter = "", ""
        while "exit" not in keyword:
            keyword = input(
                "Please enter a keyword and confirm with enter, type 'exit' to exit: "
            )
            filter += keyword.lower()
            filter += ","
        data["filter"] = filter.replace(",exit,", "")
    else:
        data["filter"] = ""

    wbm_logger.logging.info("Done! Writing config file..")

    with open("config.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def next_page(curr_page_num):
    if driver.find_elements(
        By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul/li[4]/a"
    ):
        page_list = driver.find_element(
            By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul"
        )
        wbm_logger.logging.info(
            f"Another page of flats was detected, switching to page {curr_page_num +1}/{len(page_list.find_elements(By.TAG_NAME, 'li'))-2}.."
        )
        try:
            page_list.find_elements(By.TAG_NAME, "li")[curr_page_num + 1].click()
            return curr_page_num + 1
        except:
            wbm_logger.logging.error("Failed to switch page, returning to main page..")
            return curr_page_num
    else:
        wbm_logger.logging.error(f"Failed to switch page, lastpage reached..")
        return curr_page_num


def continue_btn():
    wbm_logger.logging.info("Looking for continue button..")
    continue_btn = flat_elem.find_element(By.XPATH, '//*[@title="Details"]')
    wbm_logger.logging.info(f"Flat link found: ", continue_btn.get_attribute("href"))
    continue_btn.location_once_scrolled_into_view
    driver.get(continue_btn.get_attribute("href"))


def fill_form(email):
    wbm_logger.logging.info(f"Filling out form for email adress '{email}' ..")
    driver.find_element(
        By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[1]/div/div/div[1]/label'
    ).click()
    driver.find_element(By.XPATH, '//*[@id="powermail_field_wbsgueltigbis"]').send_keys(
        user.wbs_date
    )
    driver.find_element(
        By.XPATH, '//*[@id="powermail_field_wbszimmeranzahl"]'
    ).send_keys(user.wbs_rooms)
    driver.find_element(
        By.XPATH,
        '//*[@id="powermail_field_einkommensgrenzenacheinkommensbescheinigung9"]',
    ).send_keys(user.wbs_num)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_name"]').send_keys(
        user.last_name
    )
    driver.find_element(By.XPATH, '//*[@id="powermail_field_vorname"]').send_keys(
        user.first_name
    )
    driver.find_element(By.XPATH, '//*[@id="powermail_field_strasse"]').send_keys(
        user.street
    )
    driver.find_element(By.XPATH, '//*[@id="powermail_field_plz"]').send_keys(
        user.zip_code
    )
    driver.find_element(By.XPATH, '//*[@id="powermail_field_ort"]').send_keys(user.city)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_e_mail"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_telefon"]').send_keys(
        user.phone
    )
    driver.find_element(
        By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[14]/div/div/div[1]/label'
    ).click()


# check if config exists, else start setup
if os.path.isfile("config.yaml"):
    wbm_logger.logging.info("Loading config..")
    with open("config.yaml", "r") as config:
        try:
            user = User(yaml.safe_load(config))
        except yaml.YAMLError as exc:
            wbm_logger.logging.error("Error opening config file! ")
else:
    wbm_logger.logging.warning(f"No config file found, starting setup..")
    setup()
    wbm_logger.logging.info("Loading config..")
    with open("config.yaml", "r") as config:
        try:
            user = User(yaml.safe_load(config))
        except yaml.YAMLError as exc:
            wbm_logger.logging.error("Error opening config file! ")

if not os.path.isfile("log.txt"):
    open("log.txt", "a").close()

start_url = (
    f"file://{os.getcwd()}/test-data/wohnung_mehrere_seiten.html"
    if TEST
    else "https://www.wbm.de/wohnungen-berlin/angebote/"
)


while True:

    wbm_logger.logging.info(f"Connecting to ", start_url)

    # If we are on same page as last iteration, there probably is only one page or last page was reached and we want to reload the first page
    if not page_changed:
        driver.get(start_url)
        curr_page_num = 1
        prev_page_num = 1

    # Check if cookie dialog is displayed and accept if so
    if (
        len(
            driver.find_elements(
                By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]'
            )
        )
        > 0
    ):
        wbm_logger.logging.info("Accepting cookies..")
        driver.find_element(
            By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]'
        ).click()

    # Find all flat offers displayed on current page
    wbm_logger.logging.info("Looking for flats..")
    all_flats = driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")

    # If there is at least one flat start further checks
    if all_flats:

        wbm_logger.logging.info(f"Found {len(all_flats)} flat(s) in total:")

        # For every flat do checks
        for i in range(0, len(all_flats)):

            time.sleep(1.5)

            # We need to generate the flat_elem every iteration because otherwise they will go stale for some reason
            all_flats = driver.find_elements(
                By.CSS_SELECTOR, ".row.openimmo-search-list-item"
            )
            flat_elem = all_flats[i]

            # Create flat object
            flat_obj = flat(flat_elem.text)

            # Open log file
            with open("log.txt", "r") as myfile:
                log = myfile.read()

            # Check if we already applied to flat by looking for its unique hash in the log file
            for email in user.email:

                # We need to generate the flat_elem every iteration because otherwise they will go stale for some reason
                all_flats = driver.find_elements(
                    By.CSS_SELECTOR, ".row.openimmo-search-list-item"
                )
                flat_elem = all_flats[i]
                if (str(flat_obj.hash) + str(email).strip()) not in log:

                    # Check if we omit flat because of filter keyword contained
                    if any(
                        str(keyword).strip() in flat_elem.text.lower()
                        for keyword in user.filter
                    ):
                        wbm_logger.logging.warning(
                            f"Ignoring flat '{flat_obj.title}' because it contains filter keyword(s)."
                        )
                        break
                    else:
                        wbm_logger.logging.info(f"Title: ", flat_obj.title)

                        # Find and click continue button on current flat
                        continue_btn()

                        # Fill out application form on current flat using info stored in user object
                        fill_form(str(email).strip())

                        # Submit form
                        driver.find_element(
                            By.XPATH,
                            '//*[@id="c722"]/div/div/form/div[2]/div[15]/div/div/button',
                        ).click()

                        # Write flat info to log file
                        with open("log.txt", "a") as myfile:
                            myfile.write(
                                f"[{constants.today}] - ID: {id}\nApplication sent for flat:\n{flat_obj.title}\n{flat_obj.street}\n{flat_obj.city + ' ' + flat_obj.zip_code}\ntotal rent: {flat_obj.total_rent}\nflat size: {flat_obj.size}\nrooms: {flat_obj.rooms}\nwbs: {flat_obj.wbs}\nhash: {flat_obj.hash}{str(email).strip()}\n\n"
                            )

                        # Increment id (not really used anymore)
                        id += 1
                        wbm_logger.logging.info("Done!")

                        time.sleep(1.5)
                        driver.get(start_url)
                else:
                    # Flats hash was found in log file
                    wbm_logger.logging.warning(
                        f"Oops, we already applied for flat: {flat_obj.title}, with ID: {id}!"
                    )
                    break

            # We checked all flats on this page, try to switch to next page if exists. This should be called in last iteration
            if i == len(all_flats) - 1:
                prev_page_num = curr_page_num
                curr_page_num = next_page(curr_page_num)
                page_changed = curr_page_num != prev_page_num

    else:
        # List of flats is empty there is no flat displayed on current page
        wbm_logger.logging.info("Currently no flats available :(")

    if not page_changed:
        time.sleep(int(args.interval) * 60)
    else:
        time.sleep(1.5)

    wbm_logger.logging.info("Reloading main page..")

# driver.quit()
