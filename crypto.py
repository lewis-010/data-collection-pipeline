from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import json

class Scraper():
    def __init__(self):
        self.link_number = 0 # number of links that will be taken from the webpage
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    
 
    # accept cookies on crypto.com homepage
    def accept_cookies(self) -> webdriver.Chrome:
        driver = self.driver
        driver.get('https://crypto.com/eea')
        driver.maximize_window()
        time.sleep(3)
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')


    # navigate to the price page that displays the top 50 coins by market cap
    def navigate_to_prices(self):
        driver = self.driver
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/main/div[1]/div/div/div/div[1]/a/button"))).click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1]) # switch to new window (shows top 50 coins)
        except TimeoutException:
            print('Loading timed out.')


    # skip the tour of the price page
    def skip_tour(self):
        driver = self.driver
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')
        

    # get links for the top 50 coins by market cap
    def get_list_of_coin_links(self) -> list:
        driver = self.driver
        table = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1v8x7dw [href]")))
        table = driver.find_elements(by=By.CSS_SELECTOR, value=".css-1v8x7dw [href]")
        links = [elem.get_attribute('href') for elem in table]
        print(links)
        self.link_number = len(links)
        print(f"There are {self.link_number} links.")

        return links


    # get data for crypto ID, market cap, price and 24 change
    def get_data(self, link):
        driver = self.driver
        dict_data = {}
        driver.get(link)
        ID  = driver.find_element(by=By.CSS_SELECTOR, value = ".css-1xvru47").text
        dict_data['ID'] = ID
        print(ID)
        market_cap = driver.find_element(by=By.CSS_SELECTOR, value = ".css-1c8c51m").text
        dict_data['market cap'] = market_cap
        print(market_cap)
        time.sleep(1)
        price = str(driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/h2/span").text)
        new_price = price.replace("USD","")
        dict_data['price'] = new_price  
        print(new_price)
        time.sleep(1)
        change = driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/p[1]").text
        dict_data['24H change'] = change
        print(change)
        # include timestamp in each dict
        timestamp = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')
        dict_data['timestamp'] = timestamp

        return dict_data


    def quit(self):
        driver = self.driver
        driver.quit()


# call all methods and iterate through the list of links
if __name__=="__main__":
    crypto = Scraper()
    crypto.accept_cookies()
    crypto.navigate_to_prices()
    crypto.skip_tour()
    link_list = []
    link_list.extend(crypto.get_list_of_coin_links())
    data_list = []
    for link in range(50):
        coin_link = link_list[link] # link to a cryptocurrency (e.g., ethereum) details page where data is scraped
        coin = crypto.get_data(link=coin_link)
        data_list.append(coin)
    crypto.quit()

# print list of dicts on new line
print(*data_list, sep = "\n")

# save list of dictts to raw_data folder
with open("raw_data/data.json", "w") as f:
    json.dump(data_list, f, sep = "\n")
