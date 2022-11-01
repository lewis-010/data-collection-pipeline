from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# accept cookies on coinmarket homepage
def accept_cookies() -> webdriver.Chrome:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://coinmarketcap.com/')
    driver.maximize_window()
    time.sleep(3)
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cmc-cookie-policy-banner']/div[2]"))).click()
        time.sleep(3)
    except TimeoutException:
        print('Loading timed out.')
    
    return driver