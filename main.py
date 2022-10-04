#!/usr/bin/env python3

from email.policy import default
import sys, time, datetime, hashlib, yaml, os.path
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-H", "--headless_off", action='store_false', help="If set, turn off headless run. The bot will run in the opened browser.")
parser.add_argument("-t", "--test", action='store_true', help="If set, run test-run on the test data. This does not actually connect to wbm.de.")
parser.add_argument("-i", "--interval", default=5, help="Set the time interval in minutes to check for new flats on wbm.de. [default: 5]")

args = parser.parse_args()


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.headless = args.headless_off
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(5)

def date():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y - %H:%M')


flats = []
id = 0
curr_page_num = 1
page_changed = False
TEST = args.test
if TEST: print("------------------TEST RUN------------------")

class Flat:
  def __init__(self, flat_elem):
      flat_attr = flat_elem.split('\n')
      self.title = flat_attr[0]
      self.district = flat_attr[4]
      self.street = flat_attr[5]
      self.zip_code = flat_attr[6].split(' ')[0]
      self.city = flat_attr[6].split(' ')[1]
      self.total_rent = flat_attr[8]
      self.size = flat_attr[10]
      self.rooms = flat_attr[12]
      self.wbs = True if ('wbs' in flat_elem or 'WBS' in flat_elem) else False
      self.hash = hashlib.sha256(flat_elem.encode('utf-8')).hexdigest()

class User:
  def __init__(self, config):
      self.first_name = config['first_name']
      self.last_name = config['last_name']
      self.street = config['street']
      self.zip_code = config['zip_code']
      self.city = config['city']
      self.email = config['email'].split(',')
      self.phone = config['phone']
      self.wbs = True if 'yes' in config['wbs'] else False
      self.wbs_date = config['wbs_date'].replace('/', '')
      self.wbs_rooms = config['wbs_rooms']
      self.filter = config['filter'].split(',')
      
      if '100' in config['wbs_num']:
        self.wbs_num = 'WBS 100'
      elif '140' in config['wbs_num']:
        self.wbs_num = 'WBS 140'
      elif '160' in config['wbs_num']:
        self.wbs_num = 'WBS 160'
      elif '180' in config['wbs_num']:
        self.wbs_num = 'WBS 180'
      else:
        self.wbs_num = ''


def setup():
    data = {}
    data['first_name'] = input("Please input your first name and confirm with enter: ")
    data['last_name'] = input("Please input your last name and confirm with enter: ")
    email, email_ls, c = '', '', 1
    while 'exit' not in email:
        email = input(f"Please input email adress {c} and confirm with enter, type 'exit' to exit: ")
        email_ls += email.lower()
        email_ls += ','
        c += 1
    data['email'] = email_ls.replace(',exit,','')
    data['street'] = input("Please input your street and confirm with enter or leave empty and skip with enter: ")
    data['zip_code'] = input("Please input your zip_code and confirm with enter or leave empty and skip with enter: ")
    data['city'] = input("Please input your city and confirm with enter or leave empty and skip with enter: ")
    data['phone'] = input("Please input your phone number and confirm with enter or leave empty and skip with enter: ")
    data['wbs'] = input("Do you have a WBS (Wohnberechtigungsschein)?\nPlease type yes / no: ")
    if 'yes' in data['wbs']:
        data['wbs_date'] = input("Until when will the WBS be valid?\nPlease enter the date in format month/day/year: ")
        data['wbs_num'] = input("What WBS number (Einkommensgrenze nach Einkommensbescheinigung § 9) does your WBS show?\nPlease enter WBS 100 / WBS 140 / WBS 160 / WBS 180: ")
        data['wbs_rooms'] = input("For how many rooms is your WBS valid?\nPlease enter a number: ")
    else:
        data['wbs_date'] = ''
        data['wbs_num'] = ''
        data['wbs_rooms'] = ''
    if 'yes' in input("Do you want to enter keywords to exclude specific flats from the search results?\nPlease type yes / no: "):
        keyword, filter = '', ''
        while 'exit' not in keyword:
            keyword = input("Please enter a keyword and confirm with enter, type 'exit' to exit: ")
            filter += keyword.lower()
            filter += ','
        data['filter'] = filter.replace(',exit,','')
    else:
        data['filter'] = ''

    print(f"[{date()}]Done! Writing config file..")

    with open('config.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def next_page(curr_page_num):
    if driver.find_elements(By.XPATH, '/html/body/main/div[2]/div[1]/div/nav/ul/li[4]/a'):
        page_list = driver.find_element(By.XPATH, "/html/body/main/div[2]/div[1]/div/nav/ul")
        print(f"[{date()}] Another page of flats was detected, switching to page {curr_page_num +1}/{len(page_list.find_elements(By.TAG_NAME, 'li'))-2}..")
        try:
            page_list.find_elements(By.TAG_NAME, 'li')[curr_page_num + 1].click()
            return curr_page_num + 1
        except:
            print(f"[{date()}] Failed to switch page, returning to main page..")
            return curr_page_num
    else:
        print(f"[{date()}] Failed to switch page, lastpage reached..")
        return curr_page_num

def continue_btn():
    print(f"[{date()}] Looking for continue button..")
    continue_btn = flat_elem.find_element(By.XPATH, '//*[@title="Details"]')
    print(f"[{date()}] Flat link found: ", continue_btn.get_attribute('href'))
    continue_btn.location_once_scrolled_into_view
    driver.get(continue_btn.get_attribute('href'))

def fill_form(email):
    print(f"[{date()}] Filling out form for email adress '{email}' ..")
    driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[1]/div/div/div[1]/label').click()
    driver.find_element(By.XPATH, '//*[@id="powermail_field_wbsgueltigbis"]').send_keys(user.wbs_date)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_wbszimmeranzahl"]').send_keys(user.wbs_rooms)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_einkommensgrenzenacheinkommensbescheinigung9"]').send_keys(user.wbs_num)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_name"]').send_keys(user.last_name)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_vorname"]').send_keys(user.first_name)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_strasse"]').send_keys(user.street)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_plz"]').send_keys(user.zip_code)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_ort"]').send_keys(user.city)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_e_mail"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="powermail_field_telefon"]').send_keys(user.phone)
    driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[14]/div/div/div[1]/label').click()

# check if config exists, else start setup
if os.path.isfile("config.yaml"):
    print(f"[{date()}] Loading config..")
    with open("config.yaml", "r") as config:
        try:
            user = User(yaml.safe_load(config))
        except yaml.YAMLError as exc:
            print(f"[{date()}] Error opening config file! ")
else:
    print(f"[{date()}] No config file found, starting setup..")
    setup()
    print(f"[{date()}] Loading config..")
    with open("config.yaml", "r") as config:
        try:
            user = User(yaml.safe_load(config))
        except yaml.YAMLError as exc:
            print(f"[{date()}] Error opening config file! ")

if not os.path.isfile('log.txt'): open('log.txt', 'a').close()

start_url = f"file://{os.getcwd()}/test-data/wohnung_mehrere_seiten.html" if TEST else "https://www.wbm.de/wohnungen-berlin/angebote/"


while True:

    print(f"[{date()}] Connecting to ", start_url)

    # If we are on same page as last iteration, there probably is only one page or last page was reached and we want to reload the first page
    if not page_changed:
        driver.get(start_url)
        curr_page_num = 1
        prev_page_num = 1

    # Check if cookie dialog is displayed and accept if so
    if len(driver.find_elements(By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]')) > 0:
        print(f"[{date()}] Accepting cookies..")
        driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]').click()
    
    # Find all flat offers displayed on current page
    print(f"[{date()}] Looking for flats..")
    all_flats = driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")
    
    # If there is at least one flat start further checks
    if all_flats:

        print(f"[{date()}] Found {len(all_flats)} flat(s) in total:")

        # For every flat do checks
        for i in range(0,len(all_flats)):
            
            time.sleep(1.5)

            # We need to generate the flat_elem every iteration because otherwise they will go stale for some reason
            all_flats = driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")
            flat_elem = all_flats[i]
            
            # Create flat object
            flat = Flat(flat_elem.text)

            # Open log file
            with open("log.txt", "r") as myfile:
                log = myfile.read()
            
            # Check if we already applied to flat by looking for its unique hash in the log file
            for email in user.email:

                # We need to generate the flat_elem every iteration because otherwise they will go stale for some reason
                all_flats = driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")
                flat_elem = all_flats[i]
                if (str(flat.hash) + str(email).strip()) not in log:

                    # Check if we omit flat because of filter keyword contained
                    if any(str(keyword).strip() in flat_elem.text.lower() for keyword in user.filter):
                        print(f"[{date()}] Ignoring flat '{flat.title}' because it contains filter keyword(s).")
                        break
                    else:
                        print(f"[{date()}] Title: ", flat.title)

                        # Find and click continue button on current flat
                        continue_btn()

                        # Fill out application form on current flat using info stored in user object
                        fill_form(str(email).strip())
                        
                        # Submit form
                        driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[15]/div/div/button').click()

                        # Write flat info to log file
                        with open("log.txt", "a") as myfile:
                            myfile.write(f"[{date()}] - ID: {id}\nApplication sent for flat:\n{flat.title}\n{flat.street}\n{flat.city + ' ' + flat.zip_code}\ntotal rent: {flat.total_rent}\nflat size: {flat.size}\nrooms: {flat.rooms}\nwbs: {flat.wbs}\nhash: {flat.hash}{str(email).strip()}\n\n")

                        # Increment id (not really used anymore)
                        id += 1
                        print(f"[{date()}] Done!")
                        
                        time.sleep(1.5)
                        driver.get(start_url)
                else:
                    # Flats hash was found in log file
                    print(f"[{date()}] Oops, we already applied for flat: {flat.title}, with ID: {id}!")
                    break

            # We checked all flats on this page, try to switch to next page if exists. This should be called in last iteration
            if i == len(all_flats)-1: 
                prev_page_num = curr_page_num
                curr_page_num = next_page(curr_page_num)
                page_changed = curr_page_num != prev_page_num

    else:
        # List of flats is empty there is no flat displayed on current page
        print(f"[{date()}] Currently no flats available :(")

    if not page_changed : 
        time.sleep(int(args.interval) * 60)
    else:
        time.sleep(1.5)

    print(f"[{date()}] Reloading main page..")

#driver.quit()
