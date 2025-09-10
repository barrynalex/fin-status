import os
import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dotenv import load_dotenv

class Bank():
    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.driver = self.get_driver()
        info = self.get_info()
        for key, value in info.items():
            setattr(self, key, value)


    def get_info(self):
        load_dotenv()
        info = dict()
        info['ID'] = os.getenv("ID")
        info['userID'] = os.getenv(f"{self.name}_userid")
        info['password'] = os.getenv(f"{self.name}_password")

        return info

    def get_driver(self):
        # Automatically download and update ChromeDriver
        chrome_driver_path = ChromeDriverManager().install()
        
        # Create a Service object for ChromeDriver
        service = Service(chrome_driver_path)

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-data-dir=~/fin-status/my-user-profile")

        # Initialize the driver with the service object
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def close_driver(self):
        self.driver.close()
        logging.info(f"{self.name} logout successful!!")