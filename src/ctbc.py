from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from credential.credential import ctbc_userid, ctbc_password, ID

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

def main():
    driver = update_chrome()

    driver.get("https://www.ctbcbank.com/twrbc/twrbc-general/ot001/010")
    driver.implicitly_wait(20)
    custid_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[1]/div/input")
    userid_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[2]/div/input")
    password_box = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[3]/div/input")
    login_button = driver.find_element(By.XPATH, "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/div/a[1]")

    custid_box.send_keys(ID)
    userid_box.send_keys(ctbc_userid)
    password_box.send_keys(ctbc_password)
    login_button.click()

    input("Press Enter to quit.....")
    driver.quit()

def update_chrome():
    # Automatically download and update ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()
    
    # Create a Service object for ChromeDriver
    service = Service(chrome_driver_path)

    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-blink-features")
    # Initialize the driver with the service object
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == "__main__":
    main()
