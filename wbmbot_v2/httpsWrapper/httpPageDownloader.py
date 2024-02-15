import logging
import os
import warnings

import requests
from pywebcopy import save_webpage
from utility import io_operations

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


def download_pdf_file(url: str, local_dir: str) -> None:
    """
    Download a PDF file from the given URL to the local directory.

    Args:
        url (str): The URL of the PDF to be downloaded.
        local_dir (str): The local directory path to save the downloaded PDF.

    Returns:
        None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if response is not OK

        io_operations.create_directory_if_not_exists(local_dir)
        file_name = url.split("/")[-1]
        file_path = os.path.join(local_dir, file_name)

        with open(file_path, "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pdf_file.write(chunk)

    except requests.exceptions.RequestException as e:
        None
