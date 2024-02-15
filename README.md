- [WBMBOT\_v2](#wbmbot_v2)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Configuration File Example](#configuration-file-example)
  - [Outputs](#outputs)
  - [Command-Line Interface](#command-line-interface)
  - [Docker](#docker)
    - [Building](#building)
    - [Pull](#pull)
    - [Run](#run)
  - [Filtering Strategy](#filtering-strategy)
  - [Logging](#logging)
  - [Additional Information](#additional-information)
  - [TODO](#todo)

# WBMBOT_v2

> An improved work-in-progress (WIP) and fully refactored version of the original [WBMBOT by David Fischer](https://github.com/fischer-hub/wbmbot).

WBMBOT_v2 is a Selenium-based Python bot designed to automate the application process for new flats listed by WBM Wohnungsbaugesellschaft Berlin-Mitte GmbH. It prioritizes speed and efficiency to ensure your application is among the first 1000 considered in the random selection process for apartment viewings.

## Prerequisites

- Python 3.10 or higher

## Installation

To set up your environment and install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Quick Start

To launch the bot, navigate to the project directory and execute:

```bash
python3 wbmbot_v2/main.py
```

On the first run, the bot will guide you through a setup process to gather necessary information for applications on wbm.de. This data will be stored in a local `configs/wbm_config.json` file in a human-readable format.

**Security Notice**: The information is saved unencrypted. Ensure the security of your `configs/wbm_config.json` file.

Alternatively, you can manually create the `configs/wbm_config.json` file with the following structure:

### Configuration File Example

```json
{
    "first_name": "JOHN",
    "last_name": "DOE",
    "sex": "m",
    "emails": [
        "XXX@protonmail.com",
        "YYY@protonmail.com"
    ],
    "street": "Doner-Str. 123",
    "zip_code": "12345",
    "city": "Berlin",
    "phone": "4911223344",
    "wbs": "yes",
    "wbs_date": "23/04/1972",
    "wbs_num": "WBS 160",
    "wbs_rooms": "2",
    "wbs_special_housing_needs": "no",
    "filter": ["wbs", "2-zimmer", "2 zimmer", "2 zim", "2-zim"]
}
```

## Outputs

You will get outputs such as:

- Angebote HTML page (Entire HTML page) saved under `offline_viewings/angebote_pages` if ANY flats are found
- EXPOSE PDF saved under `offline_viewings/apartments_expose_pdfs` if the bot applies to a flat

All of these files are saved per bot page-check. e.g. if the angebote page has at least 1 flat, everytime the bot wants to check that page it will download under a nested folder with date and time as its name.

Remember to do a clean-up if you don't want to view them!

## Command-Line Interface

```bash
usage: main.py [-i INTERVAL] [-H] [-t]

Automates the application process for flats on the 'WBM Angebote' page, respecting user-defined exclusion filters.

options:
  -h, --help            Show this help message and exit.
  -i INTERVAL, --interval INTERVAL
                        Set the refresh interval in 'minutes' for checking new flats on wbm.de. [default: 3 minutes]
  -H, --headless_off    Disable headless mode. The bot will run in a visible browser window.
  -t, --test            Perform a test run using test data. Does not connect to wbm.de.
```

## Docker

### Building

>docker build -f ci/docker/Dockerfile -t wbmbot_v2 .

### Pull

>docker pull vel7an/wbmbot_v2:latest

### Run

If running for the first time, use `-it` to setup your config, if you already have the config ready in the correct directory, use `-d`
```bash
docker run -it \
    -v /PATH_HERE/offline_viewings:/home/offline_viewings \
    -v /PATH_HERE/logging:/home/logging \
    -v /PATH_HERE/configs:/home/configs \
    wbmbot_v2:latest
```

## Filtering Strategy

The filter list is designed to exclude listings based on specified keywords. Simply add your exclusion keywords to the list.

## Logging

Successful applications are recorded in `logging/successful_applications.txt`.

**Important**: This log prevents reapplication to the same flats. Do not delete it unless you intend to reapply to all available flats.

## Additional Information

During setup, you can provide multiple email addresses. The bot will apply to each flat once per email address. By default, the bot refreshes wbm.de every `3 minutes` to check for new listings.

As of now, there are no timeouts, bot checks, or captchas on the website (which we hope remains the case). However, given the limited number of flats available, frequent checks are not deemed necessary compared to platforms like immoscout24.

*Embark on your apartment hunt with WBMBOT_v2. Good luck!*

## TODO

- [X] **HIGH PRIORITY** Fix form filling
- [X] **HIGH PRIORITY** Fix `next page` logic
- [X] Add the reason if ignoring a flat (To make sure your filters are working properly) in logging
- [ ] Change "successful_applications.txt" to JSON type
- [ ] Add support for multi user wbm_config files
- [ ] Fix test-data
- [ ] Make a portable docker image of the bot that can be hosted anywhere
- [ ] Add "excluded_applications.json" that shows all applications that were excluded by the filter
- [X] Add color_printer class into the works with the logger
- [ ] Notify via e-mail whenever the bot applies to an application
- [X] Download the 'Angebote' page as an HTML for records keeping
- [X] Download the viewing of an apartment as a PDF (Available on WBM) for records keeping
- [ ] Automatically detect if internet network connection is down and pause/restart once back
- [X] Make a docker container out of the bot
- [ ] Make an compiled exec of the bot
- [ ] CI/CD for Github (?)