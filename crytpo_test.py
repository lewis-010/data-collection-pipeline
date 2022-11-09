from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import crypto
import unittest

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_accept_cookies(self):
        driver = self.driver
        

    def tearDown(self):
        self.driver.close()

if __name__=='__main__':
    unittest.main()