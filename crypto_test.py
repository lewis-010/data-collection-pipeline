from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import crypto

Crypto = crypto.Scraper() # allows crytpo.py methods to be called and tested

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())   

    def test_accept_cookies(self):
        Crypto.accept_cookies()
        try:
            cookies_banner = WebDriverWait(Crypto.driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-banner-sdk']")))
        except TimeoutException:
            return
        raise Exception('Cookies pop-up has not disappeared')
    
    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    unittest.main()