from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# navigates to the explore page on coinbase, displaying the top 30 coins by market-cap
def navigate_to_explore():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.coinbase.com')
    driver.maximize_window()
    time.sleep(3)

    button = driver.find_element_by_id('header-price-link')
    button.click()

navigate_to_explore()