from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import crypto

Crypto = crypto.Scraper() # allows crypto.py methods to be called and tested

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())   

    def test_accept_cookies(self):
        Crypto.accept_cookies()
        cookies_banner = Crypto.driver.find_element(by=By.XPATH, value = "//*[@id='onetrust-banner-sdk']")
        style_attribute = cookies_banner.get_attribute('style')
        self.assertIn('hidden', style_attribute)
        print('The accept cookies button has been clicked')      
        
    def test_navigate_to_prices(self):
        Crypto.navigate_to_prices()
        new_tab = Crypto.driver.find_element(by=By.XPATH, value = '/html')
        style_attribute = new_tab.get_attribute('class')
        self.assertIn('js-focus-visible', style_attribute)
        print('The driver has switched to the new tab')

    def test_skip_tour(self):
        Crypto.skip_tour()   
        try:
            tour = Crypto.driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div") 
            class_attribute = tour.get_attribute('class')
            self.assertNotIn('css-k008qs', class_attribute)
        except NoSuchElementException:
            print('The skip tour button has been clicked.')
            return False            
        return True
    
    def test_get_list_of_coin_links(self):
        Crypto.get_list_of_coin_links()
        self.assertIsInstance(Crypto.links, list)
        print('The returned variable is a list')
        



    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    # unittest.main()
    test = TestCrypto()
    test.setUp()
    test.test_accept_cookies()
    test.test_navigate_to_prices()
    test.test_skip_tour()
    test.test_get_list_of_coin_links()