from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import crypto
import time
import unittest


class TestCrypto(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Firefox(executable_path = GeckoDriverManager().install())
        self.Crypto = crypto.Scraper()  

    def test_1_accept_cookies(self):
        self.Crypto.accept_cookies()
        cookies_banner = self.Crypto.driver.find_element(by=By.XPATH, value = "//*[@id='onetrust-banner-sdk']")
        style_attribute = cookies_banner.get_attribute('style')
        self.assertIn('hidden', style_attribute)
        print('The accept cookies button has been clicked.')      
        
    def test_2_navigate_to_prices(self):
        self.Crypto.navigate_to_prices()
        new_tab = self.Crypto.driver.find_element(by=By.XPATH, value = '/html')
        style_attribute = new_tab.get_attribute('class')
        self.assertIn('js-focus-visible', style_attribute)
        print('The driver has switched to the new tab.')

    def test_3_skip_tour(self):
        self.Crypto.skip_tour()   
        try:
            tour = self.Crypto.driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div") 
            class_attribute = tour.get_attribute('class')
            self.assertNotIn('css-k008qs', class_attribute)
        except NoSuchElementException:
            print('The skip tour button has been clicked.')
    
    def test_4_get_list_of_coin_links(self):
        self.Crypto.get_list_of_coin_links()
        self.assertIsInstance(self.Crypto.links, list)
        print('get_list_of_coins returns a list variable.')
    
    def test_5_get_data(self):
        self.Crypto.get_data(link='https://crypto.com/price/bitcoin')
        self.assertIsInstance(self.Crypto.dict_data, dict)
        print('get_data returns a dictionary variable.')
    
    def test_6_update_dataset(self):
        self.Crypto.driver.back()
        time.sleep(1)
        self.Crypto.update_dataset()
        self.assertIsInstance(self.Crypto.data_list, list)
        print('update_dataset returns a list variable.')
        count = len([ele for ele in self.Crypto.data_list if isinstance(ele, dict)])
        print(f'The data_list has {count} elements that are all dictionaries.')

    def tearDown(self):
        self.Crypto.driver.quit()

if __name__=='__main__':
    unittest.main()