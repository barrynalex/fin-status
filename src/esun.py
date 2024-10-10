import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from credential.credential import esun_userid, esun_password, ID

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

def main():
    #update chrome driver
    driver = update_chrome()
    #login to bank account
    driver = login(driver)
    sleep(10)


    ntd_num = driver.find_element(By.XPATH, '//*[@id="fms01002:grid_DataGridBody"]/tbody/tr[3]/td[3]').text
    foreign_num = driver.find_element(By.XPATH, '//*[@id="fms01003:grid_DataGridBody"]/tbody/tr[4]/td[3]/span[2]').text
    # pwd_box = driver.find_element(By.ID, "loginform:pxsswd")
    # login_button = driver.find_element(By.ID, "loginform:linkCommand")
    logging.info(f"ntd_num:{ntd_num}\nforeign_num:{foreign_num}")

    input("Press Enter to quit.....")
    driver.quit()

    return ntd_num, foreign_num

def login(driver):
    driver = update_chrome()

    driver.get("https://ebank.esunbank.com.tw/index.jsp")
    iframe = driver.find_element(By.ID, 'iframe1')
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(20)
    custid_box = driver.find_element(By.ID, "loginform:custid")
    name_box = driver.find_element(By.ID, "loginform:name")
    pwd_box = driver.find_element(By.ID, "loginform:pxsswd")
    login_button = driver.find_element(By.ID, "loginform:linkCommand")

    custid_box.send_keys(ID)
    name_box.send_keys(esun_userid)
    pwd_box.send_keys(esun_password)
    login_button.click()

    return driver


def update_chrome():
    # Automatically download and update ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()
    
    # Create a Service object for ChromeDriver
    service = Service(chrome_driver_path)

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-blink-features")

    # Initialize the driver with the service object
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    main()
