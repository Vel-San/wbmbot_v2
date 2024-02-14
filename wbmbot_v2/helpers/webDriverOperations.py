import time

from handlers import flat
from helpers import constants
from logger import wbm_logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utility import io_operations


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
            By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul/li[4]/a"
        )

        # If the next page button is found, click it and log the action
        if next_page_button:
            page_list = web_driver.find_element(
                By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul"
            )
            total_pages = (
                len(page_list.find_elements(By.TAG_NAME, "li")) - 2
            )  # Adjust for non-page list items
            wbm_logger.logging.info(
                f"Another page of flats was detected, switching to page {current_page + 1}/{total_pages}.."
            )
            next_page_button.click()
            return current_page + 1
    except NoSuchElementException as e:
        # Log an error if the next page button is not found
        wbm_logger.logging.error("Failed to switch page, last page reached..")
    except Exception as e:
        # Log any other exceptions that occur
        wbm_logger.logging.error(
            f"Failed to switch page, returning to main page.. Exception: {e}"
        )

    # Return the current page number if navigation to the next page was not possible
    return current_page


def continue_btn(web_driver, flat_element):
    """
    Finds and clicks the 'continue' button to navigate to the details page of a flat.

    This function searches for a button with the title "Details", logs its href attribute,
    scrolls it into view, and navigates to the linked details page.
    """

    try:
        # Log the attempt to find the continue button
        wbm_logger.logging.info("Looking for continue button..")

        # Attempt to find the continue button by its XPath
        continue_button = flat_element.find_element(By.XPATH, '//*[@title="Details"]')

        # Log the href attribute of the found button
        flat_link = continue_button.get_attribute("href")
        wbm_logger.logging.info(f"Flat link found: {flat_link}")

        # Scroll the button into view
        continue_button.location_once_scrolled_into_view

        # Navigate to the href of the continue button
        web_driver.get(flat_link)
    except NoSuchElementException as e:
        # Log an error if the continue button is not found
        wbm_logger.logging.error("Continue button not found.")


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
        wbm_logger.logging.info(f"Filling out form for email address '{email}' ..")

        # Click the radio button or checkbox before filling in text fields
        web_driver.find_element(
            By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[1]/div/div/div[1]/label'
        ).click()

        # Fill in the user's WBS date
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_wbsgueltigbis"]'
        ).send_keys(user_obj.wbs_date)

        # Fill in the user's WBS rooms
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_wbszimmeranzahl"]'
        ).send_keys(user_obj.wbs_rooms)

        # Fill in the user's WBS number
        web_driver.find_element(
            By.XPATH,
            '//*[@id="powermail_field_einkommensgrenzenacheinkommensbescheinigung9"]',
        ).send_keys(user_obj.wbs_num)

        # Fill in the user's last name
        web_driver.find_element(By.XPATH, '//*[@id="powermail_field_name"]').send_keys(
            user_obj.last_name
        )

        # Fill in the user's first name
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_vorname"]'
        ).send_keys(user_obj.first_name)

        # Fill in the user's street address
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_strasse"]'
        ).send_keys(user_obj.street)

        # Fill in the user's postal code
        web_driver.find_element(By.XPATH, '//*[@id="powermail_field_plz"]').send_keys(
            user_obj.zip_code
        )

        # Fill in the user's city
        web_driver.find_element(By.XPATH, '//*[@id="powermail_field_ort"]').send_keys(
            user_obj.city
        )

        # Fill in the email address
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_e_mail"]'
        ).send_keys(email)

        # Fill in the user's phone number
        web_driver.find_element(
            By.XPATH, '//*[@id="powermail_field_telefon"]'
        ).send_keys(user_obj.phone)

        # Click the submit button or another radio button/checkbox if necessary
        # This part of the code is assumed based on the initial pattern and should be adjusted if the actual form differs
        web_driver.find_element(
            By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[14]/div/div/div[1]/label'
        ).click()

    except NoSuchElementException as e:
        # Log an error if any element is not found
        wbm_logger.logging.error(
            f"Element not found during form filling. Exception: {e}"
        )


def accept_cookies(web_driver):
    """
    Check if the cookie dialog is displayed on the page and accept it if present.

    Parameters:
    - driver: The Selenium WebDriver instance to interact with the browser.
    - logger: A logging.Logger instance for logging messages.

    Returns:
    - None
    """

    try:
        # Define the XPath for the 'Accept Cookies' button
        accept_button_xpath = '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]'

        # Wait for the cookie dialog to be present and clickable
        WebDriverWait(web_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
        )

        # Click the 'Accept Cookies' button
        web_driver.find_element(By.XPATH, accept_button_xpath).click()
        wbm_logger.logging.info("Cookies have been accepted.")
    except TimeoutException as e:
        # If the cookie dialog does not appear within the timeout, log a message
        wbm_logger.logging.warning("No cookie dialog appeared within the timeout.")


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
    return (str(flat_obj.hash) + str(email).strip()) in log


def contains_filter_keywords(flat_elem, user_filters):
    """Check if the flat contains any of the filter keywords."""
    return any(
        str(keyword).strip() in flat_elem.text.lower() for keyword in user_filters
    )


def apply_to_flat(web_driver, flat_element, user_profile, email):
    """Apply to the flat using the provided email."""
    # Find and click continue button on current flat
    continue_btn(web_driver, flat_element)

    # Fill out application form on current flat using info stored in user object
    fill_form(web_driver, user_profile, email)

    # Submit form
    web_driver.find_element(
        By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[15]/div/div/button'
    ).click()


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

    if not page_changed:
        current_page, previous_page = reset_to_start_page(
            web_driver, start_url, current_page, previous_page
        )

    accept_cookies(web_driver)

    # Find all flat offers displayed on current page
    wbm_logger.logging.info("Looking for flats..")
    all_flats = find_flats(web_driver)
    if not all_flats:
        wbm_logger.logging.info("Currently no flats available 😔")
        return

    wbm_logger.logging.info(f"Found {len(all_flats)} flat(s) in total.")
    log_content = io_operations.read_log_file(constants.log_file_path)

    for i, flat_elem in enumerate(all_flats):
        time.sleep(1.5)  # Sleep to mimic human behavior and avoid detection

        flat_obj = flat.Flat(flat_elem.text)  # Create flat object

        for email in user_profile.emails:
            if not check_flat_already_applied(flat_obj, email, log_content):
                if contains_filter_keywords(flat_elem, user_profile.filter):
                    wbm_logger.logging.warning(
                        f"Ignoring flat '{flat_obj.title}' because it contains filter keyword(s)."
                    )
                    break
                else:
                    wbm_logger.logging.info(f"Applying to flat: {flat_obj.title}")
                    apply_to_flat(web_driver, flat_elem, user_profile, email)
                    log_entry = f"[{constants.today}] - Application sent for flat: {flat_obj.title}\n"
                    io_operations.write_log_file(constants.log_file_path, log_entry)
                    wbm_logger.logging.info("Done!")
                    time.sleep(1.5)
                    web_driver.get(start_url)
            else:
                wbm_logger.logging.warning(
                    f"Oops, we already applied for flat: {flat_obj.title}!"
                )
                break

        # Try to switch to next page if exists, in the last iteration
        if i == len(all_flats) - 1:
            previous_page = current_page
            current_page = next_page(current_page)
            page_changed = current_page != previous_page

    if not page_changed:
        time.sleep(int(refresh_internal) * 60)
    else:
        time.sleep(1.5)

    wbm_logger.logging.info("Reloading main page..")
