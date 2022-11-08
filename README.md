# The Data Collection Project
With the amount of data in our lives growing exponentially, data analytics has become a hugely important part of the way businesses and organisations are run. Therefore, companies need analysts who can scrape the web for data in sophisticated and efficient ways. Web scraping allows data to be collected and collated in specific formats from the internet which can then be used to help make informed business decisions. 

This project will focus on the data collection aspect of a chosen website, [Crytpo.com](https://crypto.com/eea) using [Selenium](https://www.selenium.dev/) and [Chromedriver](https://chromedriver.chromium.org/) to automate the data scraping.

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