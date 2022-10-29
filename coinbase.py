from selenium import webdriver
import time

# navigates to the explore page on coinbase, displaying the top 30 coins by market-cap
def navigate_to_explore():
    driver = webdriver.Chrome()
    driver.get("https://www.coinbase.com")

