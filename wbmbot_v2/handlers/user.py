import json


class User:
    """
    A class to represent a user profile.

    This class takes a JSON string representing user configuration details and assigns
    user attributes based on the parsed JSON object.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        street (str): The street address of the user.
        zip_code (str): The postal code for the user's location.
        city (str): The city where the user is located.
        emails (list of str): A list of email addresses for the user.
        phone (str): The phone number of the user.
        wbs (bool): A boolean indicating if the user has a Wohnberechtigungsschein (WBS).
        wbs_date (str): The date associated with the user's WBS, formatted without slashes.
        wbs_rooms (str): The number of rooms associated with the user's WBS.
        filter (list of str): A list of filter preferences for the user.
        wbs_num (str): A string representing the user's WBS number category.
    """

    def __init__(self, json_config):
        """
        Constructs all the necessary attributes for the user object.

        Parameters:
            json_config (str): A JSON string containing user configuration details.
        """
        self.config = json_config  # Parse the JSON string into a dictionary

        self.first_name = self.config.get("first_name", "")
        self.last_name = self.config.get("last_name", "")
        self.street = self.config.get("street", "")
        self.zip_code = self.config.get("zip_code", "")
        self.city = self.config.get("city", "")
        self.emails = self.config.get("emails", [])
        self.phone = self.config.get("phone", "")
        self.wbs = "yes" in self.config.get("wbs", "").lower()
        self.wbs_date = self.config.get("wbs_date", "").replace("/", "")
        self.wbs_rooms = self.config.get("wbs_rooms", "")
        self.filter = self.config.get("filter", [])

        # Determine the WBS number category based on the provided wbs_num value
        wbs_num = self.config.get("wbs_num", "")
        if "100" in wbs_num:
            self.wbs_num = "WBS 100"
        elif "140" in wbs_num:
            self.wbs_num = "WBS 140"
        elif "160" in wbs_num:
            self.wbs_num = "WBS 160"
        elif "180" in wbs_num:
            self.wbs_num = "WBS 180"
        else:
            self.wbs_num = ""
