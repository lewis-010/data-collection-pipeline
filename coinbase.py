from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# accept cookies on coinbase homepage
def accept_cookies() -> webdriver.Chrome:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.coinbase.com')
    driver.maximize_window()
    time.sleep(3)
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div[2]/button[2]"))).click()
        time.sleep(3)
    except TimeoutException:
        print('Loading timed out.')
    
    return driver

# navigate to the explore page that displays the top 30 coins by market cap
def navigate_to_explore(driver: webdriver.Chrome):
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/header/div[2]/div/div[2]/nav/a[1]/div/span"))).click()
        time.sleep(3)
    except TimeoutException:
        print('Loading timed out.')
    
    return driver

# get links for the top 30 coins by market cap
def get_links(driver: webdriver.Chrome) -> list:
    coin = driver.find_element(by=By.XPATH, value="//*[@id='main']/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div/table/tbody/tr[1]") # doesn't work
    a_tag = coin.find_element(by=By.TAG_NAME, value='a')
    link = a_tag.get_attribute('href')
    print(link)

if __name__=="__main__":
    driver = accept_cookies()
    navigate_to_explore(driver)
    get_links(driver)
