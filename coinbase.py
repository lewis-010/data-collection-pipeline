from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# navigates to the explore page on coinbase, displaying the top 30 coins by market-cap
def navigate_to_explore():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.coinbase.com")
    driver.maximize_window()
    time.sleep(10)

navigate_to_explore()