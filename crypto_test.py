from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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
        skip_tour_tab = Crypto.driver.find_element(by=By.XPATH, value = "//*[@id='__next']/div[3]/div[2]")
        self.assertNotIn(skip_tour_tab)
        print('The skip tour button has been clicked.')

# //*[@id="__next"] id of whole page
# //*[@id="__next"]/div[3]/div[2] id of tab that goes

    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    unittest.main()