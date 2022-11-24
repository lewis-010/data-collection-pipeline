# The Data Collection Project
With the amount of data in our lives growing exponentially, data analytics has become a hugely important part of the way businesses and organisations are run. Therefore, companies need analysts who can scrape the web for data in sophisticated and efficient ways. Web scraping allows data to be collected and collated in specific formats from the internet which can then be used to help make informed business decisions. 

This project will focus on the data collection aspect of a chosen website, [Crytpo.com](https://crypto.com/eea) using [Selenium](https://www.selenium.dev/) and [Geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox to automate the data scraping.

## Milestone 1
- The data of interest on the chosen site was key information on the top 50 crytocurrencies by market cap, in particular their name, market cap, price and 24H change.
- A blank scraper class was created to be populated with the methods needed to get the necessary data.
- Initial methods:
    - Accept cookies by using Selenium's built in .click() feature.
    - Navigate to the price page by using Selenium's built in .click() feature.
    - Skip tour of the price page by using Selenium's built in .click() feature.
- For all the methods above, Selenium located the required button through the XPATH of the element that was taken from the HTML of the webpage.
<br/><br>

## Milestone 2
- The most efficient way to scrape data from each of the cryptocurrencies would be to iterate through a list of links for the details page of each coin.
- The top 50 coins by market cap are displayed on the price page (already navigate to) and each contain an href attribute that specifies the URL of the details page for each coin.
- A method was created to scrape these links and put them into a list using Selenium's *find_elements* and* *get_attribute* features.
```Python
table = driver.find_elements(by=By.CSS_SELECTOR, value=".css-1v8x7dw [href]")
links = [elem.get_attribute('href') for elem in table]
```

## Milestone 3
- With a list of links created, a method to collect the data from these links was written.
- A list of dictionaries for each coin containing the data points mentioned earlier was created as the output for this method.
- Each data point has its own XPATH within the HTML, however, for some of the pages in the list, this XPATH was slightly different.
- Therefore, for some most of the data points, the CSS_SELECTOR was used as the locator as this didn't differ between any of the links. 
```Python
market_cap = driver.find_element(by=By.CSS_SELECTOR, value = ".css-1c8c51m").text
dict_data['market cap'] = market_cap
```
## Milestone 4
- The final step was to implement code that would iterate through the list of links and get the required data.
- This method also executes the methods that get a list of links and get data from said links.  
```Python
link_list = []
link_list.extend(Scraper.get_list_of_coin_links(self))
self.data_list = []
    for link in range(50):
        coin_link = link_list[link] # link to a cryptocurrency (e.g., ethereum) details page where data is scraped
        coin = Scraper.get_data(self, link=coin_link)
        self.data_list.append(coin)
```
- Finally, the *data_list* was saved to a *raw_data* folder in .json file.
- This allows for future analysis of the data.
```Python
with open("raw_data/data.json", "w") as file:
    json.dump(data_list, file, indent=2)
```
## Milestone 5
- Once the code for the scraper had been written, the next stage was to create a file that would run all of the unit tests for main python file.  
- Some of these tests focused on identifying changes in the HTML that occured when a method was executed, and using this change to assert if the method had been executed properly.
    - For example, the *accept cookies* method is teted by asserting the style attribute of the cookies banner has changed to hidden.
```Python
def test_1_accept_cookies(self):
    Crypto.accept_cookies()
    cookies_banner = Crypto.driver.find_element(by=By.XPATH, value = "//*   [@id='onetrust-banner-sdk']")
    style_attribute = cookies_banner.get_attribute('style')
    self.assertIn('hidden', style_attribute)
    print('The accept cookies button has been clicked.') 
```
- Other tests focused on asserting the returned variable from a method is of the right type.
    - For instance, the *update dataset* method is tested by asserting all elements in the *data_list* are dictionaries.
```Python
def test_6_update_dataset(self):
    Crypto.driver.back()
    time.sleep(3)
    Crypto.update_dataset()
    self.assertIsInstance(Crypto.data_list, list)
    print('update_dataset returns a list variable.')
    count = len([ele for ele in Crypto.data_list if isinstance(ele, dict)])
    print(f'The data_list has {count} elements that are all dictionaries.')
    Crypto.quit()
```
## Milestone 6
- The final part of this project was to take steps that allows the scraper to be run on the cloud and to create a CI/CD pipeline.
- A docker image was created for the *crypto.py* file, the container for this was then pushed to [Dockerhub](https://www.docker.com/products/docker-hub/).
    - A requirement for this was to adjust the code for the scraper so that it can run in "headless" mode without the GUI.
    - The code for creating the docker image can be found in *Dockerfile*.
