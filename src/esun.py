import logging
from time import sleep
from bank import Bank
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

class esun(Bank):
    def get_number(self):
        self.login()
        sleep(10)

        ntd_num = self.driver.find_element(By.XPATH, '//*[@id="fms01002:grid_DataGridBody"]/tbody/tr[3]/td[3]').text
        foreign_num = self.driver.find_element(By.XPATH, '//*[@id="fms01003:grid_DataGridBody"]/tbody/tr[4]/td[3]/span[2]').text
        logging.info(f"ntd_num:{ntd_num}\nforeign_num:{foreign_num}")

        # input("Press Enter to quit.....")
        self.driver.quit()

        return ntd_num, foreign_num

    def login(self):
        driver = self.driver

        driver.get("https://ebank.esunbank.com.tw/index.jsp")
        iframe = driver.find_element(By.ID, 'iframe1')
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(20)
        custid_box = driver.find_element(By.ID, "loginform:custid")
        name_box = driver.find_element(By.ID, "loginform:name")
        pwd_box = driver.find_element(By.ID, "loginform:pxsswd")
        login_button = driver.find_element(By.ID, "loginform:linkCommand")

        custid_box.send_keys(self.ID)
        name_box.send_keys(self.userID)
        pwd_box.send_keys(self.password)
        login_button.click()
        logging.info(f"{self.name} login successful!!")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    client = esun("esun")
    twd_number, foreign_number = client.get_number()
