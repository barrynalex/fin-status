import logging
import ddddocr
from time import sleep
from bank import Bank
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

class ipost(Bank):
    def get_number(self):
        self.login()
        sleep(10)

        ntd_num = self.driver.find_element(By.XPATH, '//*[@id="css_table2"]/div[2]/div[3]/span').text

        logging.info(f"ntd_num:{ntd_num}")

        # input("Press Enter to quit.....")
        self.driver.quit()

        return ntd_num

    def login(self):
        driver = self.driver

        driver.get("https://ipost.post.gov.tw/pst/home.html")

        # locate all the elements
        driver.implicitly_wait(20)
        # click pop up element
        pop_up_element = driver.find_element(By.XPATH, '//*[@id="modal"]/div[2]/button')
        pop_up_element.click()
        sleep(3)

        custid_box = driver.find_element(By.ID, "cifID")
        name_box = driver.find_element(By.ID, "userID_1_Input")
        pwd_box = driver.find_element(By.ID, "userPWD_1_Input")
        login_button = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[12]/a')
        image_element = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[14]/img')
        image_element.screenshot("code_image.png")
        validation_box = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[11]/input')
        replace_image_button = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[14]/a')

        ocr = ddddocr.DdddOcr(show_ad=False)

        image = open("code_image.png", "rb").read()
        code = ocr.classification(image)

        tries = 0
        while True:
            # input ids and password
            custid_box.send_keys(self.ID)
            name_box.send_keys(self.userID)
            pwd_box.send_keys(self.password)
            # input validation code
            image_element.screenshot("code_image.png")
            image = open("code_image.png", "rb").read()
            code = ocr.classification(image)
            validation_box.send_keys(code)
            login_button.click()
            tries += 1
            if tries > 10:
                break

            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(alert.text)
                alert.accept()
                replace_image_button.click()
                sleep(10)
            except Exception as e:
                print(e)
                logging.info(f"{self.name} login successful!!")
                break

        # input("Press Enter to quit.....")




if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    client = ipost("ipost")
    ntd_num = client.get_number()
