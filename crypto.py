from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import datetime
import json

class Scraper():
    '''Contains various functions to perform webscraping operations on a given webpage'''
    
    def __init__(self, driver = webdriver.Firefox or webdriver.Chrome):
        '''
        Attributes
        ----------
        link_number: int
            The number of links of individual crytpocurrency pages to be scraped
        links: list
            A list of links to be iteratively scraped for data
        dict_data: dict
            A dictionary containing scraped data for an individual link
        data_list: list
            A list of individual dictionaries
        driver: WebDriver
            The webdriver to be used for scraping data
        '''
        self.link_number = 0
        self.links = []
        self.dict_data = {}
        self.data_list = []
        
        self.driver = driver
        if self.driver == webdriver.Chrome:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--headless")
            self.options.add_argument("window-size=1920,1080")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--disable-setuid-sandbox") 
            self.options.add_argument('--disable-gpu')
            self.options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = self.options)
        
        else:
            self.options = webdriver.FirefoxOptions()
            self.options.add_argument('--headless')       
            self.driver = webdriver.Firefox(executable_path = GeckoDriverManager().install(), options = self.options)

 
    def accept_cookies(self):
        '''Clicks the 'accept cookies' button on the cryto.com homepage to allow the webdriver to continue'''
        self.driver.get('https://crypto.com/eea')
        self.driver.maximize_window()
        try:
            WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
        except TimeoutException:
            print('Loading timed out.')


    def navigate_to_prices(self):
        '''Clicks the 'prices' tab on the crypo.com homepage to display the top 50 coins by market cap'''
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/main/div[1]/div/div/div/div[1]/a/button"))).click()
            self.driver.switch_to.window(self.driver.window_handles[1]) # switch to new window (shows top 50 coins)
        except TimeoutException:
            print('Loading timed out.')


    def skip_tour(self):
        '''Clicks the 'skip tour' button on the price page to allow the webdriver to continue'''
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div"))).click()
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
        table = self.driver.find_elements(by=By.CSS_SELECTOR, value=".css-1v8x7dw [href]")
        self.links = [elem.get_attribute('href') for elem in table]
        self.link_number = len(self.links)
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
        self.dict_data = {}
        self.driver.get(link)
        id  = (self.driver.find_element(by=By.CSS_SELECTOR, value = ".css-1xvru47").text)
        self.dict_data['ID'] = id
        market_cap = self.driver.find_element(by=By.CSS_SELECTOR, value = ".css-1c8c51m").text
        self.dict_data['market_cap'] = market_cap
        price = str(self.driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/h2/span").text)
        new_price = price.replace("USD","")
        self.dict_data['price'] = new_price
        change = self.driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/p[1]").text
        self.dict_data['24H_change'] = change
        timestamp = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')
        self.dict_data['timestamp'] = timestamp
        return self.dict_data


    def update_dataset(self):
        '''
        Iteratively scrapes data from the list of links collected in the previous method.

        Returns
        -------
        data_list: list
            A JSON file containing a list of dictionaries with the data scraped from each link.
        '''
        link_list = []
        link_list.extend(self.get_list_of_coin_links())
        self.data_list = []
        for link in range(len(link_list)):
            coin_link = link_list[link] # link to a cryptocurrency (e.g., ethereum) details page where data is scraped
            coin = self.get_data(coin_link)
            self.data_list.append(coin)
            
        print(*self.data_list, sep = "\n")
        with open("raw_data/data.json", "w") as file: # save list of dicts to raw_data folder
            json.dump(self.data_list, file, indent=2)


    def quit(self):
        '''Closes the browser window and stops the webdriver from running'''
        self.driver.quit()
        

if __name__=="__main__":
    crypto = Scraper()
    crypto.accept_cookies()
    crypto.navigate_to_prices()
    crypto.skip_tour()
    crypto.update_dataset()
    crypto.quit()