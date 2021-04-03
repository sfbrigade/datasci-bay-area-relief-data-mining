    ### notes

# if 403 error: pretend i'm firefox's open-source renderer
    # r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# find single (find) vs all
    # soup.find_all(x)

# print formatted html
    # print(soup.prettify())

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

### automate the google search 
### in separate file to keep testing separate
from googlesearcher import Grants
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
class AutomateGoogle():
    def load_with_selenium(self, query: str) -> str:
        # bay%20area%20covid%20business%20grants
        driver.get('https://www.google.com/search?hl=en&as_q={}&as_qdr=m&as_occt=any&safe=images'.format(urllib.parse.quote_plus(query)))
        # google_search = driver.find_elements_by_name("btnK")[1]
        # driver.implicitly_wait(100)
        # ActionChains(driver).move_to_element(google_search).click(google_search).perform()

    def pull_out_results(self):
        soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'lxml')
        h3_results = soup.find_all('h3')
        if len(h3_results) > 0:
            with open('result.txt', 'a') as results:
                for info in h3_results:
                    if 'href' in info.parent.attrs:
                        url = info.parent.attrs['href'] + '\n'
                        print(url)
                        results.write(url)

    def get_next_page(self) -> str:
        next = driver.find_elements_by_id('pnnext')[0]
        driver.implicitly_wait(100)
        ActionChains(driver).move_to_element(next).click(next).perform()

automator = AutomateGoogle()
automator.load_with_selenium('sf bay area covid business grants')
automator.pull_out_results()
for i in range(10):
    automator.get_next_page()
    automator.pull_out_results()

automator.load_with_selenium('sf bay area covid business loans')
automator.pull_out_results()
for i in range(10):
    automator.get_next_page()
    automator.pull_out_results()
driver.quit()
# soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
# h3_results = soup.find_all('h3')
# if len(h3_results) > 0:
#     with open('result.txt', 'a') as results:
#         for info in h3_results:
#             if 'href' in info.parent.attrs:
#                 url = info.parent.attrs['href'] + '\n'
#                 print(url)
#                 results.write(url)
# next = driver.find_elements_by_id('pnnext')[0]
# driver.implicitly_wait(100)
# ActionChains(driver).move_to_element(next).click(next).perform()
# soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
# h3_results = soup.find_all('h3')
# if len(h3_results) > 0:
#     with open('result.txt', 'a') as results:
#         for info in h3_results:
#             if 'href' in info.parent.attrs:
#                 url = info.parent.attrs['href'] + '\n'
#                 print(url)
#                 results.write(url)
# next = driver.find_elements_by_id('pnnext')[0]
# driver.implicitly_wait(100)
# ActionChains(driver).move_to_element(next).click(next).perform()
# soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
# h3_results = soup.find_all('h3')
# if len(h3_results) > 0:
#     with open('result.txt', 'a') as results:
#         for info in h3_results:
#             if 'href' in info.parent.attrs:
#                 url = info.parent.attrs['href'] + '\n'
#                 print(url)
#                 results.write(url)
# next = driver.find_elements_by_id('pnnext')[0]
# driver.implicitly_wait(100)
# ActionChains(driver).move_to_element(next).click(next).perform()
# soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
# h3_results = soup.find_all('h3')
# if len(h3_results) > 0:
#     with open('result.txt', 'a') as results:
#         for info in h3_results:
#             if 'href' in info.parent.attrs:
#                 url = info.parent.attrs['href'] + '\n'
#                 print(url)
#                 results.write(url)
# next = driver.find_elements_by_id('pnnext')[0]
# driver.implicitly_wait(100)
# ActionChains(driver).move_to_element(next).click(next).perform()
# soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
# h3_results = soup.find_all('h3')
# if len(h3_results) > 0:
#     with open('result.txt', 'a') as results:
#         for info in h3_results:
#             if 'href' in info.parent.attrs:
#                 url = info.parent.attrs['href'] + '\n'
#                 print(url)
#                 results.write(url)
# google_search_results_web = Grants().get_search_results()
# soup = BeautifulSoup(google_search_results_web.text, "lxml")
# for info in soup.find_all('h3'):
#     print(info.text)
#     print('-----')


def scrape_url(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")

    ### extract links from website into data structure
    ### maybe store in dictionary not array?
    links = []
    urls = []

    ### using get_text() method
    ### href = True instead of using attrs - not sure why this works instead?
    ### does not contain logic to weed out anything that links to the same tmc website

    ### grab visible webpage text not svg / imgs
        ### Scalable Vector Graphics (SVG) are an XML-based markup language for describing two-dimensional based vector graphics
        ### in window._wpemojiSettings dictionary try: no 'svgUrl'
        ### path tag/attribute - almost always svg (there's also an svg tag)
        ### extract to remove unwanted tags before you get text
    for link in soup.find_all('a', href=True):  
        #### BeautifulSoup converts the values of the attribute class in a list eg. <div class="ABC BCD CDE123"> soup.div['class'] --> ['ABC', 'BCD', 'CDE123']

        # get just the domain of the url
            
        #### link.svg returns either svg or None
        if link.svg:
            print("ignore, this has svg")
        else:
            print(link)
            links.append(link)
            urls.append(link.attrs['href'])
        
    for url in urls:
        print("url:", url)

### testing w/ just the first link


### this works - reinstate after testing
# for grant in grants_list:
#     url = grant
#     scrape_url(url)






### note: filter out any non-bay area

### get info from each of those links (goal is pulling all info about grants)
# for key in links:
    ### could turn this bit into a helper function
    # url = links[key]
    # r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    # soup = BeautifulSoup(r.text, "html.parser")

    ### try using regex to find what we're searching for?
    # searched_word = 'deadline'
    
    # for link in soup.find_all(string=re.compile('.*{0}.*'.format(searched_word), recursive=True)):
    #     print(soup.prettify())


    

### general logic:
# if page says 'closed' or some variant on 'no longer accepting applications'
    # return closed
# elif the word 'deadline' or ?? is on the page
    # return the deadline
# elif there's another link that says apply
    # scrape that link for the deadline
        # same logic above, if closed return closed otherwise share the date or not avail
# else
    # some message like 'check the webpage for details' or 'not available'

    








