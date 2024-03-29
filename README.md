![Docker Pulls](https://img.shields.io/docker/pulls/vel7an/wbmbot_v2?style=flat-square&logo=docker&label=DOCKER%20PULLS) ![Docker Image Size](https://img.shields.io/docker/image-size/vel7an/wbmbot_v2?style=flat-square&logo=docker&label=IMAGE%20SIZE)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/vel-san/wbmbot_v2?style=flat-square&logo=github&label=COMMITS) ![GitHub repo size](https://img.shields.io/github/repo-size/vel-san/wbmbot_v2?style=flat-square&logo=github&label=REPO%20SIZE) ![GitHub forks](https://img.shields.io/github/forks/vel-san/wbmbot_v2?style=flat-square&logo=github&label=FORKS) ![GitHub Repo stars](https://img.shields.io/github/stars/vel-san/wbmbot_v2?style=flat-square&logo=github&label=STARS) ![GitHub commits since latest release](https://img.shields.io/github/commits-since/vel-san/wbmbot_v2/latest?sort=date&style=flat-square&logo=github&label=COMMITS%20SINCE%20LAST%20RELEASE)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/vel-san/wbmbot_v2/docker-build-push.yml?style=flat-square&logo=github&label=BUILD%20STATUS)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/vel-san/wbmbot_v2/check-leaks.yml?style=flat-square&logo=github&label=SECRETS%20LEAKS) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/vel-san/wbmbot_v2/github-code-scanning%2Fcodeql?style=flat-square&logo=github&label=CODE%20QUALITY)

![Code Format](https://img.shields.io/badge/CODE%20FORMAT-BLACK-black?style=flat-square&logo=python)

![GitHub Release](https://img.shields.io/github/v/release/vel-san/wbmbot_v2?sort=date&display_name=tag&style=flat-square&logo=semver&label=BOT%20VERSION&color=teal)

![Alt](https://repobeats.axiom.co/api/embed/ab658dc363a9401ed4e7171a5442d8e1c1fe585b.svg "Repobeats analytics image")

- [WBMBOT\_v2](#wbmbot_v2)
  - [IMPORTANT DISCLAIMER](#important-disclaimer)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Configuration File Example](#configuration-file-example)
  - [Notifications (E-mails)](#notifications-e-mails)
  - [Outputs](#outputs)
  - [Command-Line Interface](#command-line-interface)
  - [Docker](#docker)
    - [Build](#build)
    - [Pull](#pull)
    - [Run](#run)
      - [Without e-mail notifications](#without-e-mail-notifications)
      - [With e-mail notifications](#with-e-mail-notifications)
  - [Filtering Strategy](#filtering-strategy)
  - [Logging](#logging)
  - [Additional Information](#additional-information)
  - [TODO](#todo)


# WBMBOT_v2

> An improved work-in-progress (WIP) and fully refactored version of the original [WBMBOT by David Fischer](https://github.com/fischer-hub/wbmbot).

WBMBOT_v2 is a Selenium-based Python bot designed to automate the application process for new flats listed by WBM (Wohnungsbaugesellschaft Berlin-Mitte) GmbH. It prioritizes speed and efficiency to ensure your application is among the first to be considered in the random selection process for apartment viewings.

## IMPORTANT DISCLAIMER

The more you share this bot, the "less" your chances of finding an apartment will be. You do the math.

<details>
<summary>IN CASE YOU DON'T GET IT</summary>

>**Please do not over-share this bot to maximize your chances**

</details>


## Prerequisites

- Python 3.10 or higher
- Ubuntu Linux or Windows Docker (The bot didn't work properly on MacOS/Amazon Hosted instances)

## Installation

To set up your environment and install the required dependencies, run the following command:

```bash
pip install -r wbmbot_v2/requirements.txt
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
    "first_name": "John",
    "last_name": "Doe",
    "sex": "m",
    "emails": [
        "random_user@outlook.com"
    ],
    "notifications_email": "random_user@outlook.com",
    "street": "No-Add Str. 123",
    "zip_code": "12345",
    "city": "Berlin",
    "phone": "11223344",
    "wbs": "yes",
    "wbs_date": "23/04/1972",
    "wbs_num": "WBS 160",
    "wbs_rooms": "2",
    "wbs_special_housing_needs": "no",
    "exclude": [
        "wbs",
        "2-zimmer",
        "1-zimmer"
    ],
    "flat_rent_below": "600",
    "flat_size_above": "55",
    "flat_rooms_above": "1"
}
```

## Notifications (E-mails)

The bot will be able to send you e-mail notifications once it applies for a flat from the e-mail you input in `notifications_email` within the config.

To do so, you need to export `EMAIL_PASSWORD` to your environment variables. If this variable is not found, no e-mails will be sent.

**NOTE**: If your email has 2FA (MFA), you need to create an `App Password` from your Outlook online settings.

**NOTE**: Only `@outlook.com` emails are currently supported

```bash
export EMAIL_PASSWORD=<password>
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

A Selenium-based bot that scrapes 'WBM Angebote' page and auto applies on appartments based on user exclusion filters

options:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Set the time interval in 'minutes' to check for new flats (refresh) on wbm.de. [default: 3 minutes]
  -H, --headless        If set, use 'headless' run. The bot will run in the background, otherwise, a chrome tab will show.
  -t, --test            If set, run test-run on the test data. This does not actually connect to wbm.de.
```

## Docker

### Build

```bash
docker build -f ci/docker/Dockerfile -t wbmbot_v2 .
```

### Pull

```bash
docker pull vel7an/wbmbot_v2:latest
```

### Run

If running for the first time, use `-it` to setup your config, if you already have the config ready in the correct directory, use `-d`

If you want to send emails as well to yourself as notifications, please add `-e "EMAIL_PASSWORD=<password>"` to the command

#### Without e-mail notifications

```bash
docker run -it \
    -v /PATH_HERE/offline_viewings:/home/offline_viewings \
    -v /PATH_HERE/logging:/home/logging \
    -v /PATH_HERE/configs:/home/configs \
    vel7an/wbmbot_v2:latest
```

#### With e-mail notifications

```bash
docker run -it \
    -e "EMAIL_PASSWORD=<password>" \
    -v /PATH_HERE/offline_viewings:/home/offline_viewings \
    -v /PATH_HERE/logging:/home/logging \
    -v /PATH_HERE/configs:/home/configs \
    vel7an/wbmbot_v2:latest
```

## Filtering Strategy

The exclude list is designed to exclude listings based on specified keywords. Simply add your exclusion keywords to the list.

Alternatively you can also use the 3 variables in the config:

> "flat_rent_below": "600"
>
> "flat_size_above": "55"
>
> "flat_rooms_above": "1"

Where the bot will "include" your options only. If the rent/size/rooms is *equal* **OR** *below/above* then it will consider the flat to apply.

## Logging

Successful applications are recorded in `logging/successful_applications.json`.

**Important**: This log prevents reapplication to the same flats. ***DO NOT DELETE*** it unless you intend to re-apply to all available flats.

## Additional Information

During setup, you can provide multiple email addresses. The bot will apply to each flat once per email address. By default, the bot refreshes wbm.de every `3 minutes` to check for new listings.

As of now, there are no timeouts, bot checks, or captchas on the website (which we hope remains the case). However, given the limited number of flats available, frequent checks are not deemed necessary compared to platforms like immoscout24.

*Embark on your apartment hunt with WBMBOT_v2. Good luck!*

## TODO

- [X] **HIGH PRIORITY** Fix form filling
- [X] **HIGH PRIORITY** Fix `next page` logic
- [X] **HIGH PRIORITY** Add an `include only` filter for **zimmer numbers**, **rent cost** & **size**
- [X] Add the reason if ignoring a flat (To make sure your filters are working properly) in logging
- [X] Add color_printer class into the works with the logger
- [X] Notify via e-mail whenever the bot applies to an application
- [X] Download the 'Angebote' page as an HTML for records keeping
- [X] Download the viewing of an apartment as a PDF (Available on WBM) for records keeping
- [X] Make a docker container out of the bot
- [X] CI/CD for Github
- [X] Fix test-data
- [X] Change "successful_applications.txt" to JSON type
- [X] Automatically detect if internet network connection is down and pause/restart once back
- [ ] ~~Add support for multi user wbm_config files~~
- [ ] Add "excluded_applications.json" that shows all applications that were excluded by the filter
- [ ] Make a compiled exec of the bot using pyinstaller