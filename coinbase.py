from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def accept_cookies():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.coinbase.com')
    driver.maximize_window()
    time.sleep(3)
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div[2]/button[2]")))
    except TimeoutException:
        print('Loading timed out.')

# navigates to the explore page on coinbase, displaying the top 30 coins by market-cap
def navigate_to_explore():

    
    button = driver.find_element(by=By.XPATH, value='//button[@class="Button-sc-111z0u6-0 iaBuWF"]')
    button.click()
    time.sleep(3)

navigate_to_explore()