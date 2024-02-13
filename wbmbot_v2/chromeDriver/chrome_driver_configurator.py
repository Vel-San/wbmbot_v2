from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriverConfigurator:
    """
    Class to create the WebDriver with ChromeOptions
    """

    def __init__(self, headless_off: bool, test: bool):
        """
        Create a ChromeDriver with default options
        """
        self.headless_off = headless_off
        self.test = test
        self.chrome_options = Options()
        self.configure_options()
        self.driver = self.create_driver()

    def configure_options(self):
        """
        Add ChromeOption defaults
        """
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.headless = self.headless_off
        if self.test:
            self.chrome_options.add_argument("--log-level=0")

    def create_driver(self):
        """
        Creates the driver with the specified ChromeOptions
        """
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )
        # Wait 5 seconds before doing stuff
        driver.implicitly_wait(5)
        return driver

    def get_driver(self):
        return self.driver
