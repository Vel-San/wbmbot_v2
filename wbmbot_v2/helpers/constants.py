import datetime as dt
import os

# Today
today = dt.date.today()
# Now
now = dt.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M")

# Retrieve email and password from environment variables
email_password = os.environ.get("EMAIL_PASSWORD")

# WBM Config File Name
wbm_config_name = f"{os.getcwd()}/configs/wbm_config.json"

# Applications Logger that we applied for
log_file_path = f"{os.getcwd()}/logging/successful_applications.txt"

# Script Logging
script_log_path = f"{os.getcwd()}/logging/wbmbot-v2_{today}.log"

# Offline viewing paths
offline_angebote_path = f"{os.getcwd()}/offline_viewings/angebote_pages/"
offline_apartment_path = f"{os.getcwd()}/offline_viewings/apartments_expose_pdfs/"

# URLs
wbm_url = "https://www.wbm.de/wohnungen-berlin/angebote/"
test_wbm_url = f"file://{os.getcwd()}/test-data/wohnung_mehrere_seiten.html"
