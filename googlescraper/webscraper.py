import datetime
import pathlib

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import boto3
import os
from numpy import loadtxt
from os.path import exists

# You must download the major version code of chrome driver for your version
# of chrome on your computer: https://chromedriver.chromium.org/downloads
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

filename = '{}-result.txt'.format(datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S"))
search_permutations_filename = 'new_searches.txt'


def finished_uploading():
    print('Done uploading!')


# chrome_options.add_argument('--headless')
class AutomateGoogle():
    def load_with_selenium(self, query: str) -> str:
        driver.get('https://www.google.com/search?hl=en&as_q={}&as_qdr=m&as_occt=any&safe=images'.format(
            urllib.parse.quote_plus(query)))
        # google_search = driver.find_elements_by_name("btnK")[1]
        # driver.implicitly_wait(100)
        # ActionChains(driver).move_to_element(google_search).click(google_search).perform()

    def pull_out_results(self):
        temp_results = []
        print("filename: {}".format(filename))
        if exists(filename):
            lines = loadtxt(filename, dtype=str, comments="#", delimiter="\n", unpack=False)
            for line in lines:
                temp_results.append(line)

        print("temp_results: {}".format(temp_results))

        soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'lxml')
        h3_results = soup.find_all('h3')
        if len(h3_results) > 0:
            with open(filename, 'a') as results:
                for info in h3_results:
                    if 'href' in info.parent.attrs:
                        url = info.parent.attrs['href']
                        if url not in temp_results:
                            print("didn't find url {} in list".format(url))
                            temp_results.append(url)
                            results.write(url + "\n")
                        else:
                            print("found url {} in list".format(url))

    def get_next_page(self) -> str:
        next = driver.find_elements_by_id('pnnext')[0]
        driver.implicitly_wait(100)
        ActionChains(driver).move_to_element(next).click(next).perform()


search_template = "{} california covid {}"
locations = ["contra costa county", "santa clara county", "marin county", "alameda county", "san francisco county",
             "san mateo county", "solano county", "sonoma county", "napa county"]
services = ["business grants", "business loans", "grants", "loans", "services", "assistance"]

automator = AutomateGoogle()
for location in locations:
    for service in services:
        print("search is \'{}\'".format(search_template.format(location, service)))
        with open(search_permutations_filename, 'a') as searches:
            searches.write(search_template.format(location, service) + "\n")
        driver = webdriver.Chrome()
        automator.load_with_selenium(search_template.format(location, service))
        automator.pull_out_results()
        for i in range(2):
            automator.get_next_page()
            automator.pull_out_results()
        driver.quit()
    time.sleep(900)


# client = boto3.client('s3')
# pathlib.Path().absolute()

# for file in os.listdir():
#     if '-result.txt' in file:
#         upload_file_bucket = 'google-search-01'
#         upload_file_key = str(file)
#         try:
#             client.upload_file(file, upload_file_bucket, upload_file_key)
#         except RuntimeError as err:
#             print("File upload ran into an error {}".format(err))
#         os.remove(file)

def scrape_url(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    urls = []
    for link in soup.find_all('a', href=True):
        if link.svg:
            print("ignore, this has svg")
        else:
            print(link)
            links.append(link)
            urls.append(link.attrs['href'])

    for url in urls:
        print("url:", url)
