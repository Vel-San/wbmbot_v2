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
        exclude (list of str): A list of exclude preferences for the user.
        wbs_num (str): A string representing the user's WBS number category.
        flat_rent_below (str): A string representing the user's rent upper limit.
        flat_size_above (str): A string representing the user's flat size bottom limit.
        flat_rooms_above (str): A string representing the user's flat rooms bottom limit.
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
        self.sex = (
            "Frau"
            if self.config.get("sex", "") == "f"
            else "Herr"
            if self.config.get("sex", "") == "m"
            else "Offen"
        )
        self.street = self.config.get("street", "")
        self.zip_code = self.config.get("zip_code", "")
        self.city = self.config.get("city", "")
        self.emails = self.config.get("emails", [])
        self.notifications_email = self.config.get("notifications_email", "")
        self.phone = self.config.get("phone", "")
        self.wbs = "yes" in self.config.get("wbs", "").lower()
        self.wbs_date = self.config.get("wbs_date", "").replace("/", "")
        self.wbs_rooms = self.config.get("wbs_rooms", "")
        self.wbs_special_housing_needs = (
            "yes" in self.config.get("wbs_special_housing_needs", "").lower()
        )
        self.exclude = self.config.get("exclude", [])

        # Determine the WBS number category based on the provided wbs_num value
        self.wbs_num = self.config.get("wbs_num", "")
        if "100" in self.wbs_num:
            self.wbs_num = "WBS 100"
        elif "140" in self.wbs_num:
            self.wbs_num = "WBS 140"
        elif "160" in self.wbs_num:
            self.wbs_num = "WBS 160"
        elif "180" in self.wbs_num:
            self.wbs_num = "WBS 180"
        elif "220" in self.wbs_num:
            self.wbs_num = "WBS 220"
        elif "240" in self.wbs_num:
            self.wbs_num = "WBS 240"
        else:
            self.wbs_num = ""

        # Setup user filters to be "included" e.g. Apply to flats with rent below XX, Apply to flat with size above XX
        self.flat_rent_below = self.config.get("flat_rent_below", "")
        self.flat_size_above = self.config.get("flat_size_above", "")
        self.flat_rooms_above = self.config.get("flat_rooms_above", "")

    def __str__(self):
        output = ""
        output += f"First Name: {self.first_name}\n"
        output += f"Last Name: {self.last_name}\n"
        output += f"Sex: {self.sex}\n"
        output += f"Street: {self.street}\n"
        output += f"ZIP Code: {self.zip_code}\n"
        output += f"City: {self.city}\n"
        output += f"Emails: {', '.join(self.emails)}\n"
        output += f"Notifications Email: {self.notifications_email}\n"
        output += f"Phone: {self.phone}\n"
        output += f"WBS: {'Yes' if self.wbs else 'No'}\n"
        output += f"WBS Date: {self.wbs_date}\n"
        output += f"WBS Rooms: {self.wbs_rooms}\n"
        output += f"WBS Special Housing Needs: {'Yes' if self.wbs_special_housing_needs else 'No'}\n"
        output += f"WBS Number: {self.wbs_num}\n"
        output += f"Exclude: {', '.join(self.exclude)}\n"
        output += f"Flat Rent Below: {self.flat_rent_below}\n"
        output += f"Flat Size Above: {self.flat_size_above}\n"
        output += f"Flat Rooms Above: {self.flat_rooms_above}\n"
        return output
