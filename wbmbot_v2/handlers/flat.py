import hashlib


class Flat:
    """
    A class to represent a flat listing.

    This class takes a string representation of a flat listing, splits it by new lines,
    and assigns various attributes based on the content of each line.

    Attributes:
        title (str): The title of the flat listing.
        district (str): The district where the flat is located.
        street (str): The street address of the flat.
        zip_code (str): The postal code for the flat's location.
        city (str): The city where the flat is located.
        total_rent (str): The total rent cost for the flat.
        size (str): The size of the flat.
        rooms (str): The number of rooms in the flat.
        wbs (bool): A boolean indicating if the flat has a Wohnberechtigungsschein (WBS).
        hash (str): A SHA-256 hash of the flat listing details.
    """

    def __init__(self, flat_elem):
        """
        Constructs all the necessary attributes for the flat object.

        Parameters:
            flat_elem (str): The string representation of the flat listing.
        """
        self.flat_elem = flat_elem
        self.flat_attr = self.flat_elem.split("\n")
        self.attr_size = len(self.flat_attr)

        self.title = self.flat_attr[0] if self.attr_size > 0 else ""
        self.district = self.flat_attr[4] if self.attr_size > 4 else ""
        self.street = self.flat_attr[5] if self.attr_size > 5 else ""
        self.zip_code = self.flat_attr[6].split(" ")[0] if self.attr_size > 6 else ""
        self.city = self.flat_attr[6].split(" ")[1] if self.attr_size > 6 else ""
        self.total_rent = self.flat_attr[8] if self.attr_size > 8 else ""
        self.size = self.flat_attr[10] if self.attr_size > 10 else ""
        self.rooms = self.flat_attr[12] if self.attr_size > 12 else ""
        self.wbs = "wbs" in self.flat_elem.lower()
        self.hash = hashlib.sha256(self.flat_elem.encode("utf-8")).hexdigest()
