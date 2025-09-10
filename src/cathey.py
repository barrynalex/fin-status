import argparse
import logging
from time import sleep
from bank import Bank
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Cathey(Bank):
    def login(self):
        driver = self.driver

        driver.get("https://www.cathaybk.com.tw/mybank")
        # try:
        #     WebDriverWait(self.driver, 10).until(
        #         EC.element_to_be_clickable(
        #             (
        #                 By.XPATH,
        #                 "//*[@id='divSystemLoginMsg']/div/div/div[2]/div[2]/button",  # noqa:E501
        #             )
        #         )
        #     ).click()
        # except TimeoutException:
        #     pass

        id_box = driver.find_element(By.ID, "CustID")
        uid_box = driver.find_element(By.ID, "UserIdKeyin")
        pwd_box = driver.find_element(By.ID, "PasswordKeyin")

        id_box.send_keys(self.ID)
        uid_box.send_keys(self.userID)
        pwd_box.send_keys(self.password)


        login_button = driver.find_element(By.XPATH, "//*[@id='divCUBNormalLogin']/div[2]/button")
        login_button.click()
        logging.info(f"{self.name} LOGIN SUCCESSFUL")

    def get_number(self):
        self.login()
        sleep(5)

        ntd_num = self.driver.find_element(By.ID, 'TD-balance').text
        logging.info(f"Cathey NTD_num:{ntd_num}")

        self.close_driver()
        return ntd_num


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    client = Cathey()
    asset = client.get_number()