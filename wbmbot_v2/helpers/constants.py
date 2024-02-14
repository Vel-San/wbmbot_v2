import datetime as dt
import os

# Today
today = dt.date.today()

# WBM Config File Name
wbm_config_name = f"{os.getcwd()}/configs/wbm_config.json"

# Applications Logger that we applied for
log_file_path = f"{os.getcwd()}/logging/successful_applications.txt"

# Script Logging
script_log_path = f"{os.getcwd()}/logging/wbmbot-v2_{today}.log"

# URLs
wbm_url = "https://www.wbm.de/wohnungen-berlin/angebote/"
test_wbm_url = f"file://{os.getcwd()}/test-data/wohnung_mehrere_seiten.html"
