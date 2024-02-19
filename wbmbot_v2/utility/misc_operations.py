import requests


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


def check_internet_connection():
    """
    Check internet connection by sending a GET request to www.google.com using HTTPS.

    Returns:
        bool: True if internet connection is available, False otherwise.
    """

    try:
        response = requests.get("https://www.google.com", timeout=1)
        return response.status_code in [200, 201, 204]
    except requests.Timeout:
        return False
    except requests.ConnectionError:
        return False
    except requests.TooManyRedirects:
        return False
    except requests.InvalidURL:
        return False
    except requests.RequestException:
        return False
