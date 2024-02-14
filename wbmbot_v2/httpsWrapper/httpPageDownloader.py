import logging
import warnings

from pywebcopy import save_webpage

# Suppress PyWebCopy's logging
logging.getLogger("pywebcopy").setLevel(logging.CRITICAL)

# Suppress requests' logging
logging.getLogger("requests").setLevel(logging.CRITICAL)

# Suppress urllib3's logging
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# Suppress PyWebCopy's warning about browser opening
warnings.filterwarnings(
    "ignore", message="Opening in browser is not supported when threading is enabled!"
)


def save_viewing_offline(url: str, save_path: str, name: str):
    """
    Save a WBM viewing (if found) as an offline HTML file
    """

    # Download the webpage
    save_webpage(
        url=url,
        project_folder=save_path,
        project_name=name,
        bypass_robots=True,  # Bypass robots.txt rules
        debug=False,  # Print debug information
        open_in_browser=False,  # Open the saved page in a web browser
        delay=None,  # Set a delay between requests
        threaded=True,  # Use threading for faster download
    )
