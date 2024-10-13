import logging
import ddddocr
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from credential.credential import ipost_userid, ipost_password, ID

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

def main():
    #update chrome driver
    driver = update_chrome()
    #login to bank account
    driver = login(driver)
    # sleep(10)

    ntd_num = driver.find_element(By.XPATH, '//*[@id="css_table2"]/div[2]/div[3]/span').text

    logging.info(f"ntd_num:{ntd_num}")

    input("Press Enter to quit.....")
    driver.quit()

    # return ntd_num, foreign_num

def login(driver):
    driver = update_chrome()

    driver.get("https://ipost.post.gov.tw/pst/home.html")
    # iframe = driver.find_element(By.ID, 'iframe1')
    # driver.switch_to.frame(iframe)

    # locate all the elements
    driver.implicitly_wait(20)

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

    ocr = ddddocr.DdddOcr()

    image = open("code_image.png", "rb").read()
    code = ocr.classification(image)

    custid_box.send_keys(ID)
    name_box.send_keys(ipost_userid)
    pwd_box.send_keys(ipost_password)
    validation_box.send_keys(code)
    login_button.click()

    return driver


def update_chrome():
    # Automatically download and update ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()
    
    # Create a Service object for ChromeDriver
    service = Service(chrome_driver_path)

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize the driver with the service object
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    main()
