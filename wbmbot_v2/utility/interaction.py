import json
import os

from helpers import constants
from logger import wbm_logger

__appname__ = os.path.splitext(os.path.basename(__file__))[0]
color_me = wbm_logger.ColoredLogger(__appname__)
LOG = color_me.create_logger()


def setup_wbm_config():
    """
    Takes user-input to assemble their user profile
    """

    # Initialize a dictionary to store user data
    data = {}

    # Collect user information through input prompts
    data["first_name"] = input("Please input your first name and confirm with enter: ")
    data["last_name"] = input("Please input your last name and confirm with enter: ")
    data["sex"] = input("Please input your sex/gender (m, f, d): ")

    # Collect multiple email addresses and store them in a list
    emails = []
    while True:
        email = input(
            "Please input an e-mail address to apply with and confirm with enter, type 'exit' to exit: "
        ).lower()
        if email == "exit":
            break
        emails.append(email)
    data["emails"] = emails

    # Collect user e-mail that will be used for notifications
    data["notifications_email"] = input(
        "Please input (or leave empty) the e-mail (@outlook only) that you want to send notifications from: "
    )

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
            "What WBS number does your WBS show? Please enter WBS 100 / WBS 140 / WBS 160 / WBS 180 / WBS 220 / WBS 240: "
        )
        data["wbs_rooms"] = input(
            "For how many rooms is your WBS valid? Please enter a number: "
        )
        data["wbs_special_housing_needs"] = input(
            "Do you have special housing needs? Please type yes / no: "
        )
    else:
        data["wbs_date"] = ""
        data["wbs_num"] = ""
        data["wbs_rooms"] = ""
        data["wbs_special_housing_needs"] = ""

    # Collect keywords to exclude out specific flats
    if (
        input(
            "Do you want to enter keywords to exclude specific flats from the search results? Please type yes / no: "
        ).lower()
        == "yes"
    ):
        exclude = []
        while True:
            keyword = input(
                "Please enter a keyword and confirm with enter, type 'exit' to exit: "
            ).lower()
            if keyword == "exit":
                break
            exclude.append(keyword)
        data["exclude"] = exclude
    else:
        data["exclude"] = []

    data["flat_rent_below"] = input(
        "Please input the 'Upper Limit/Max' Rent for a flat (format: 1234): "
    )
    data["flat_size_above"] = input(
        "Please input the 'Bottom Limit/Minimum' Size for a flat (format: 123): "
    )
    data["flat_rooms_above"] = input(
        "Please input the 'Bottom Limit/Minimum' Rooms for a flat (format: 1): "
    )

    # Log the completion of data collection
    LOG.info(color_me.green("Done! Writing config file... ✅"))

    # Write the collected data to a JSON file
    with open(constants.wbm_config_name, "w") as outfile:
        json.dump(data, outfile, indent=4)
