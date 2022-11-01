from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

class Scraper():
    def __init__(self):
        self.link_number = 0 # number of links that will be taken from the webpage

    # accept cookies on crypto.com homepage
    def accept_cookies(self) -> webdriver.Chrome:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://crypto.com/eea')
        driver.maximize_window()
        time.sleep(3)
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')
        
        return driver

    # navigate to the price page that displays the top 50 coins by market cap
    def navigate_to_explore(self, driver: webdriver.Chrome):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/main/div[1]/div/div/div/div[1]/a/button"))).click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
        except TimeoutException:
            print('Loading timed out.')
        
        return driver
        

    # skip the tour of the price page
    def skip_tour(self, driver: webdriver.Chrome):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[3]/div[2]/div[2]/div[1]/div"))).click()
            time.sleep(3)
        except TimeoutException:
            print('Loading timed out.')
        
        return driver

    # get links for the top 50 coins by market cap
    def get_links(self, driver: webdriver.Chrome) -> list:
        table = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1v8x7dw [href]")))
        table = driver.find_elements(by=By.CSS_SELECTOR, value=".css-1v8x7dw [href]")
        links = [elem.get_attribute('href') for elem in table]
        print(links)
        self.link_number = len(links)
        print(f"There are {self.link_number} links.")
        driver.quit()

        return(links)

    # if __name__=="__main__":
        driver = accept_cookies()
        navigate_to_explore(driver) 
        driver.switch_to.window(driver.window_handles[1]) # swtich to latest window
        skip_tour(driver)
        get_links(driver)
        driver.quit()

crypto = Scraper()
crypto.accept_cookies()
crypto.navigate_to_explore()
crypto.skip_tour()
crypto.get_links()