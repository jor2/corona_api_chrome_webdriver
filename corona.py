from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
import time


class CoronaAPI(object):
    def __init__(self, country='Ireland'):
        self.country = country
        self.url = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'
        self.driver = webdriver.Chrome(self.driver_location, chrome_options=self.chrome_options)
        self.driver.get(self.url)
        time.sleep(1)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @property
    def chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        return chrome_options

    @property
    def driver_location(self):
        return './chromedriver'

    @property
    def all_country_statistics(self):
        return self.soup.find_all(class_='external-html')

    @property
    def confirmed_cases(self):
        raw_result = [result for result in self.all_country_statistics if self.country in result.text][0].text
        confirmed_cases = re.search(r'\n(.*?)\xa0', raw_result).group(1)
        formatted_confirmed_cases = f'{self.country}\nConfirmed Cases: {confirmed_cases}'
        return formatted_confirmed_cases


print(CoronaAPI().confirmed_cases)
