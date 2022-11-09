from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import crypto
import unittest

Crypto = crypto.Scraper() # allows crytpo.py methods to be called and tested

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())   

    def test_accept_cookies(self):
        driver = self.driver
        Crypto.accept_cookies()
        self.assertNotIn(driver.find_element(by=By.XPATH, value = "//*[@id='onetrust-accept-btn-handler']")) 
        # should pass if the XPATH of the accept cookies button is not there
        # the button has been clicked so should not be present
    
    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    unittest.main()