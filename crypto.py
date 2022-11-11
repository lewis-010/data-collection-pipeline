from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import json
import unittest

class Scraper(unittest.TestCase):
    '''Contains various functions to perform webscraping operations on a given webpage'''
    
    def __init__(self):
        '''
        Attributes
        ----------
        link_number: int
            The number of links of individual crytpocurrency pages to be scraped
        driver: WebDriver
            The webdriver to be used for scraping data
        '''
        self.link_number = 0
        self.links = None
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    
 
    def accept_cookies(self) -> webdriver.Chrome:
        '''Clicks the 'accept cookies' button on the cryto.com homepage to allow the webdriver to continue'''
        driver = self.driver
        driver.get('https://crypto.com/eea')
        driver.maximize_window()
        time.sleep(3)
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')


    def navigate_to_prices(self):
        '''Clicks the 'prices' tab on the crypo.com homepage to display the top 50 coins by market cap'''
        driver = self.driver
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/main/div[1]/div/div/div/div[1]/a/button"))).click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1]) # switch to new window (shows top 50 coins)
        except TimeoutException:
            print('Loading timed out.')


    def skip_tour(self):
        '''Clicks the 'skip tour' button on the price page to allow the webdriver to continue'''
        driver = self.driver
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')


    def get_list_of_coin_links(self):
        '''
        Gets the links for the top 50 coins by market cap
    
        Returns
        -------
        links: list
            A list of the links for the top 50 coins by market cap
        '''
        driver = self.driver
        # table = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1v8x7dw [href]")))
        time.sleep(2)
        table = driver.find_elements(by=By.CSS_SELECTOR, value=".css-1v8x7dw [href]")
        self.links = [elem.get_attribute('href') for elem in table]
        print(self.links)
        self.link_number = len(self.links)
        print(f"There are {self.link_number} links.")
        return self.links


    def get_data(self, link):
        '''
        Gets specific data the coins included in the list of links previously scraped

        Parameters
        ----------
        link: list
            The list of links for the coins that will be iteratively scraped for data

        Returns
        -------
        data_dict: dictionary
            A dicitonary containing info on name, market cap, price, 24H change and 
            timestamp of data collection for each coin
        '''
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
        timestamp = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')
        dict_data['timestamp'] = timestamp
        return dict_data


    def quit(self):
        '''Closes the browser window and stops the webdriver from running'''
        driver = self.driver
        driver.quit()
        

if __name__=="__main__":
    crypto = Scraper()
    crypto.accept_cookies()
    crypto.navigate_to_prices()
    crypto.skip_tour()
    link_list = []
    link_list.extend(crypto.get_list_of_coin_links()) # list of links to top 50 coins by market cap
    data_list = []
    for link in range(50):
        coin_link = link_list[link] # link to a cryptocurrency (e.g., ethereum) details page where data is scraped
        coin = crypto.get_data(link=coin_link)
        data_list.append(coin)
    crypto.quit()

    # print list of dicts on new line
    print(*data_list, sep = "\n")

    # save list of dicts to raw_data folder
    with open("raw_data/data.json", "w") as file:
        json.dump(data_list, file, indent=2)