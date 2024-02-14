import json

from helpers import constants
from logger import wbm_logger


def setup_wbm_config():
    """
    Takes user-input to assemble their user profile
    """

    # Initialize a dictionary to store user data
    data = {}

    # Collect user information through input prompts
    data["first_name"] = input("Please input your first name and confirm with enter: ")
    data["last_name"] = input("Please input your last name and confirm with enter: ")

    # Collect multiple email addresses and store them in a list
    emails = []
    while True:
        email = input(
            "Please input email address and confirm with enter, type 'exit' to exit: "
        ).lower()
        if email == "exit":
            break
        emails.append(email)
    data["emails"] = emails

    # Collect additional user information
    data["street"] = input(
        "Please input your street and street number and confirm with enter or leave empty and skip with enter: "
    )
    data["zip_code"] = input(
        "Please input your ZIP code and confirm with enter or leave empty and skip with enter: "
    )
    data["city"] = input(
        "Please input your city and confirm with enter or leave empty and skip with enter: "
    )
    data["phone"] = input(
        "Please input your phone number and confirm with enter or leave empty and skip with enter: "
    )

    # Collect WBS information if the user has one
    data["wbs"] = input(
        "Do you have a WBS (Wohnberechtigungsschein)? Please type yes / no: "
    ).lower()
    if data["wbs"] == "yes":
        data["wbs_date"] = input(
            "Until when will the WBS be valid? Please enter the date in format month/day/year: "
        )
        data["wbs_num"] = input(
            "What WBS number does your WBS show? Please enter WBS 100 / WBS 140 / WBS 160 / WBS 180: "
        )
        data["wbs_rooms"] = input(
            "For how many rooms is your WBS valid? Please enter a number: "
        )
    else:
        data["wbs_date"] = ""
        data["wbs_num"] = ""
        data["wbs_rooms"] = ""

    # Collect keywords to filter out specific flats
    if (
        input(
            "Do you want to enter keywords to exclude specific flats from the search results? Please type yes / no: "
        ).lower()
        == "yes"
    ):
        filters = []
        while True:
            keyword = input(
                "Please enter a keyword and confirm with enter, type 'exit' to exit: "
            ).lower()
            if keyword == "exit":
                break
            filters.append(keyword)
        data["filter"] = filters
    else:
        data["filter"] = []

    # Log the completion of data collection
    wbm_logger.logging.info("Done! Writing config file..")

    # Write the collected data to a JSON file
    with open(constants.wbm_config_name, "w") as outfile:
        json.dump(data, outfile, indent=4)
