from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import crypto
import unittest

Crypto = crypto.Scraper() # allows crytpo.py methods to be called and tested

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())   

    def test_accept_cookies(self):
        driver = self.driver
        driver.get('https://crypto.com/eea')
        driver.maximize_window()
        self.assertAlmostEqual(Crypto.accept_cookies)


    def tearDown(self):
        self.driver.close()

if __name__=='__main__':
    unittest.main()