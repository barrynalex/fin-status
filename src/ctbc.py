import logging
from bank import Bank
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
# from credential.credential import ctbc_userid, ctbc_password, ID

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

class Ctbc(Bank):
    def get_number(self):
        self.login()
        sleep(10)

        ntd_num = self.driver.find_element(By.CLASS_NAME, "txt_lg").text
        logging.info(f"ntd_num:{ntd_num}")

        # input("Press Enter to quit.....")
        self.close_driver()

        return ntd_num

    def login(self):
        driver = self.driver

        driver.get("https://www.ctbcbank.com/twrbc/twrbc-general/ot001/010")
        driver.implicitly_wait(20)
        custid_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[1]/div/input")
        userid_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[2]/div/input")
        password_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[3]/div/input")
        login_button = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/div/a[1]")

        custid_box.send_keys(self.ID)
        userid_box.send_keys(self.userID)
        password_box.send_keys(self.password)
        login_button.click()
        logging.info(f"{self.name} login successful!!")



if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    client = Ctbc()
    twd_number = client.get_number()
