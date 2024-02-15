from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriverConfigurator:
    """
    Class to create the WebDriver with ChromeOptions
    """

    def __init__(self, headless: bool, test: bool):
        """
        Create a ChromeDriver with default options
        """
        self.headless = headless
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
        self.chrome_options.add_argument("--disable-logging")
        self.chrome_options.add_argument("--log-level=3")
        if self.headless:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--no-sandbox")
        if self.test:
            self.chrome_options.add_argument("--log-level=0")

    def create_driver(self):
        """
        Creates the driver with the specified ChromeOptions
        """
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )
        # Wait 5 seconds before doing stuff
        self.driver.implicitly_wait(5)
        return self.driver

    def get_driver(self):
        return self.driver
