import os
import time

from handlers import flat
from helpers import constants, notifications
from httpsWrapper import httpPageDownloader as hpd
from logger import wbm_logger
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utility import io_operations

__appname__ = os.path.splitext(os.path.basename(__file__))[0]
color_me = wbm_logger.ColoredLogger(__appname__)
LOG = color_me.create_logger()


def next_page(web_driver, current_page: int):
    """
    Attempts to navigate to the next page of a paginated list.

    This function checks if a next page button is present and, if so, clicks it to navigate to the next page.
    It logs the action and handles any exceptions that may occur during the process.

    Parameters:
        curr_page_num (int): The current page number.

    Returns:
        int: The updated page number after attempting to navigate to the next page.
    """

    try:
        # Attempt to find the next page button using its XPath
        next_page_button = web_driver.find_element(
            By.XPATH, "//a[@title='Nächste Immobilien Seite']"
        )

        # If the next page button is found, click it and log the action
        if next_page_button:
            page_list = web_driver.find_element(
                By.XPATH, "//ul[@class='pagination pagination-sm']"
            )
            # -2 to exclude the < and > arrows of next and previous pages
            total_pages = (
                len(page_list.find_elements(By.TAG_NAME, "li")) - 2
            )  # Adjust for non-page list items
            LOG.info(
                color_me.cyan(
                    f"Another page of flats was detected, switching to page {current_page + 1}/{total_pages}"
                )
            )
            next_page_button.click()
            return current_page + 1
    except NoSuchElementException as e:
        # Log an error if the next page button is not found
        LOG.error(color_me.red("Failed to switch page, last page reached"))
    except Exception as e:
        # Log any other exceptions that occur
        LOG.error(
            color_me.red(
                f"Failed to switch page, returning to main page | Exception: {e}"
            )
        )

    # Return the current page number if navigation to the next page was not possible
    return current_page


def download_expose_as_pdf(web_driver, flat_name: str):
    """
    Gets the EXPOSE link and saves it as a PDF in your localy directory
    """

    # Log the attempt to find the continue button
    LOG.info(color_me.cyan(f"Attempting to download expose for '{flat_name}'"))

    # Attempt to find the continue button by its XPath
    download_button = web_driver.find_element(
        By.XPATH, "//a[@class='openimmo-detail__intro-expose-button btn download']"
    )

    # Log the href attribute of the found button
    download_link = download_button.get_attribute("href")

    pdf_path = hpd.download_pdf_file(
        download_link, f"{constants.offline_apartment_path}{constants.now}"
    )
    return pdf_path


def continue_btn(web_driver, flat_element):
    """
    Finds and clicks the 'continue' button to navigate to the details page of a flat.

    This function searches for a button with the title "Details", logs its href attribute,
    scrolls it into view, and navigates to the linked details page.
    """

    try:
        # Log the attempt to find the continue button
        LOG.info(color_me.cyan("Looking for continue button"))

        # Attempt to find the continue button by its XPath
        continue_button = flat_element.find_element(By.XPATH, "//a[@title='Details']")

        # Log the href attribute of the found button
        flat_link = continue_button.get_attribute("href")
        LOG.info(color_me.green(f"Flat link found: {flat_link}"))

        # Scroll the button into view
        continue_button.location_once_scrolled_into_view

        # Navigate to the href of the continue button
        web_driver.get(flat_link)
        return flat_link
    except NoSuchElementException as e:
        # Log an error if the continue button is not found
        LOG.error(color_me.red("Continue button not found."))
    except StaleElementReferenceException as e:
        # Log an error if the continue button is stale
        LOG.error(color_me.red("Stale 'Continue' button."))


def fill_form(web_driver, user_obj, email):
    """
    Fills out a web form with user information and a specified email address.

    This function locates various input fields on a web form and populates them with data from the user object.
    It also logs the process and handles any exceptions that may occur during form filling.

    Parameters:
        web_driver (WebDriver): The Selenium WebDriver used to interact with the web page.
        user (User): The user object containing data to fill the form.
        email (str): The email address to be used in the form.
    """

    try:
        # Log the start of the form filling process
        LOG.info(color_me.cyan(f"Filling out form for email address '{email}'"))

        # If the user has WBS
        if user_obj.wbs:
            # Click the radio button or checkbox before filling in text fields
            web_driver.find_element(
                By.XPATH, "//label[@for='powermail_field_wbsvorhanden_1']"
            ).click()

            # Fill in the user's WBS date
            web_driver.find_element(
                By.XPATH, "//input[@id='powermail_field_wbsgueltigbis']"
            ).send_keys(user_obj.wbs_date)

            # Fill in the user's WBS rooms
            web_driver.find_element(
                By.XPATH, "//select[@id='powermail_field_wbszimmeranzahl']"
            ).send_keys(user_obj.wbs_rooms)

            # Fill in the user's WBS number
            web_driver.find_element(
                By.XPATH,
                "//select[@id='powermail_field_einkommensgrenzenacheinkommensbescheinigung9']",
            ).send_keys(user_obj.wbs_num)

            # Click on Special Housing Needs if required
            if user_obj.wbs_special_housing_needs:
                web_driver.find_element(
                    By.XPATH,
                    "//label[@for='powermail_field_wbsmitbesonderemwohnbedarf_1']",
                ).click()
        else:
            web_driver.find_element(
                By.XPATH, "//label[@for='powermail_field_wbsvorhanden_2']"
            ).click()

        # Select the user's sex/gender
        web_driver.find_element(
            By.XPATH,
            "//select[@id='powermail_field_anrede']",
        ).send_keys(user_obj.sex)

        # Fill in the user's last name
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_name']"
        ).send_keys(user_obj.last_name)

        # Fill in the user's first name
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_vorname']"
        ).send_keys(user_obj.first_name)

        # Fill in the user's street address
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_strasse']"
        ).send_keys(user_obj.street)

        # Fill in the user's postal code
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_plz']"
        ).send_keys(user_obj.zip_code)

        # Fill in the user's city
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_ort']"
        ).send_keys(user_obj.city)

        # Fill in the email address
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_e_mail']"
        ).send_keys(email)

        # Fill in the user's phone number
        web_driver.find_element(
            By.XPATH, "//input[@id='powermail_field_telefon']"
        ).send_keys(user_obj.phone)

        # Click on Datenschutz
        web_driver.find_element(
            By.XPATH, "//label[@for='powermail_field_datenschutzhinweis_1']"
        ).click()

    except NoSuchElementException as e:
        # Log an error if any element is not found
        LOG.error(
            color_me.red(f"Element not found during form filling. Exception: {e}")
        )


def accept_cookies(web_driver):
    """
    Check if the cookie dialog is displayed on the page and accept it if present.

    Parameters:
    - driver: The Selenium WebDriver instance to interact with the browser.
    - logger: A logging.Logger instance for logging messages.

    Returns:
    - bool
    """

    try:
        # Define the XPath for the 'Accept Cookies' button
        accept_button_xpath = "//button[@class='cm-btn cm-btn-success']"

        # Wait for the cookie dialog to be present and clickable
        WebDriverWait(web_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
        )

        # Click the 'Accept Cookies' button
        web_driver.find_element(By.XPATH, accept_button_xpath).click()
        LOG.info(color_me.green("Cookies have been accepted."))
        return True
    except TimeoutException as e:
        return False


def close_live_chat_button(web_driver):
    """
    Close the 'Live Chat' dialog button
    """

    try:
        # Define the XPath for the 'Close Live Chat' button
        close_button_xpath = '//*[@id="removeConvaiseChat"]'

        # Wait for the Close Live Chat dialog to be present and clickable
        WebDriverWait(web_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, close_button_xpath))
        )

        # Click the 'Close Live Chat' button
        web_driver.find_element(By.XPATH, close_button_xpath).click()
        return True
    except TimeoutException as e:
        # If the Close Live Chat does not appear within the timeout, log a message
        return False


def reset_to_start_page(
    web_driver, start_url: str, current_page: int, previous_page: int
):
    """
    Resets the WebDriver to the start URL and resets the current and previous page counters.

    This function is typically used when the page has not changed from the last iteration,
    indicating that there is only one page or the last page was reached. It reloads the first
    page and resets the page counters.

    Parameters:
    - driver: The Selenium WebDriver instance to interact with the browser.
    - start_url: The URL of the start page to load.

    Returns:
    - curr_page_num, prev_page_num
    """

    web_driver.get(start_url)
    current_page = 1
    previous_page = 1

    return current_page, previous_page


def find_flats(web_driver):
    """Find and return a list of flats from the webpage."""

    return web_driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")


def check_flat_already_applied(flat_obj, email, log):
    """Check if an application for the flat has already been sent."""

    return (
        f"[{email.strip()}] - Application sent for flat: {flat_obj.title} | {flat_obj.hash}"
        in log
    )


def contains_filter_keywords(flat_elem, user_filters):
    """Check if the flat contains any of the filter keywords and return the keywords."""

    # Find all keywords that are in the flat_elem's text
    keywords_found = [
        keyword
        for keyword in user_filters
        if str(keyword).strip().lower() in flat_elem.text.lower()
    ]

    # Return a tuple of boolean and keywords found
    return (bool(keywords_found), keywords_found)


def apply_to_flat(web_driver, flat_element, flat_title, user_profile, email):
    """Apply to the flat using the provided email."""

    # Find and click "Ansehen" button on current flat
    flat_link = continue_btn(web_driver, flat_element)

    # Fill out application form on current flat using info stored in user object
    fill_form(web_driver, user_profile, email)

    # Download as PDF
    pdf_path = download_expose_as_pdf(web_driver, flat_title)

    # Submit form
    web_driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Send e-mail
    notifications.send_email_notification(
        email,
        f"[Applied] {flat_title}",
        f"Appartment Link: {flat_link}\n\nYour Profile: {user_profile}",
        pdf_path,
    )


def process_flats(
    web_driver,
    user_profile,
    start_url: str,
    current_page: int,
    previous_page: int,
    page_changed: bool,
    refresh_internal: int,
):
    """Process each flat by checking criteria and applying if applicable."""

    while True:
        if not page_changed:
            current_page, previous_page = reset_to_start_page(
                web_driver, start_url, current_page, previous_page
            )

        accept_cookies(web_driver)
        close_live_chat_button(web_driver)

        # Find all flat offers displayed on current page
        LOG.info(color_me.cyan("Looking for flats"))
        all_flats = find_flats(web_driver)
        if not all_flats:
            LOG.info(color_me.cyan("Currently no flats available 😔"))
            time.sleep(int(refresh_internal) * 60)
            continue

        LOG.info(color_me.green(f"Found {len(all_flats)} flat(s) in total."))
        # Save locally
        hpd.save_viewing_offline(
            start_url,
            constants.offline_angebote_path,
            f"{constants.now}/page_{current_page}",
        )
        log_content = io_operations.read_log_file(constants.log_file_path)

        for i, flat_elem in enumerate(all_flats.copy()):
            time.sleep(2)  # Sleep to mimic human behavior and avoid detection

            # Refresh Flat Elements to avoid stale
            all_flats = find_flats(web_driver)
            flat_elem = all_flats[i]

            # Create flat object
            flat_obj = flat.Flat(flat_elem.text)

            for email in user_profile.emails:
                all_flats = find_flats(web_driver)
                flat_elem = all_flats[i]
                # Proceed to check whether we should apply to the flat or skip
                if not check_flat_already_applied(flat_obj, email, log_content):
                    if contains_filter_keywords(flat_elem, user_profile.filter)[0]:
                        LOG.warning(
                            color_me.yellow(
                                f"Ignoring flat '{flat_obj.title}' because it contains filter keyword(s) --> {contains_filter_keywords(flat_elem, user_profile.filter)[1]}"
                            )
                        )
                        continue
                    else:
                        LOG.info(
                            color_me.cyan(
                                f"Applying to flat: {flat_obj.title} for '{email}'"
                            )
                        )
                        apply_to_flat(
                            web_driver, flat_elem, flat_obj.title, user_profile, email
                        )
                        log_entry = f"[{constants.today}] - [{email}] - Application sent for flat: {flat_obj.title} | {flat_obj.hash}\n"
                        io_operations.write_log_file(constants.log_file_path, log_entry)
                        LOG.info(color_me.green("Done!"))
                        time.sleep(2)
                        web_driver.get(start_url)
                else:
                    LOG.warning(
                        color_me.yellow(
                            f"Oops, we already applied for flat: {flat_obj.title}!"
                        )
                    )
                    continue

            # Try to switch to next page if exists, in the last iteration
            if i == len(all_flats) - 1:
                previous_page = current_page
                current_page = next_page(web_driver, current_page)
                page_changed = current_page != previous_page

        if not page_changed:
            time.sleep(int(refresh_internal) * 60)
        else:
            time.sleep(1.5)

        LOG.info(color_me.cyan("Reloading main page"))
