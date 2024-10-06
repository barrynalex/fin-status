from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from credential.credential import esun_userid, esun_password, ID

# chrome driver path
# chromedriver = "/usr/local/bin/chromedriver"

def main():
    driver = update_chrome()

    driver.get("https://www.ctbcbank.com/twrbc/twrbc-general/ot001/010")
    driver.implicitly_wait(5)
    custid_box = driver.find_element(By.XPATH, '/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[1]/div/input')
    # userid_box = driver.find_element(By.ID, "loginform:name")
    # password_box = driver.find_element(By.ID, "loginform:pxsswd")

    custid_box.send_keys(ID)
    # userid_box.send_keys(esun_userid)
    # password_box.send_keys(esun_password)

    input("Press Enter to quit.....")
    driver.quit()

def update_chrome():
    # Automatically download and update ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()
    
    # Create a Service object for ChromeDriver
    service = Service(chrome_driver_path)

    # Initialize the driver with the service object
    driver = webdriver.Chrome(service=service)
    return driver

if __name__ == "__main__":
    main()
