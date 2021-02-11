### notes

# if 403 error: pretend i'm firefox's open-source renderer
    # r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# find single (find) vs all
    # soup.find_all(x)

# print formatted html
    # print(soup.prettify())

import requests
from bs4 import BeautifulSoup
import re

### automate the google search 
### in separate file to keep testing separate
from googlesearcher import Grants

grants_list = Grants().get_search_results()
print(grants_list)

def scrape_url(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")

    ### extract links from website into data structure
    ### maybe store in dictionary not array?
    links = {}

    ### using get_text() method
    ### href = True instead of using attrs - not sure why this works instead?
    ### does not contain logic to weed out anything that links to the same tmc website

    ### grab visible webpage text not svg / imgs
        ### Scalable Vector Graphics (SVG) are an XML-based markup language for describing two-dimensional based vector graphics
        ### in window._wpemojiSettings dictionary try: no 'svgUrl'
        ### path tag/attribute - almost always svg (there's also an svg tag)
        ### extract to remove unwanted tags before you get text
    for link in soup.find_all('a', href=True):  
        # if 'tmcfinancing' not in tag.attrs['href']:
        
        print(link)
        links[link.get_text()] = link
    
    print(links)

for grant in grants_list:
    url = grant
    scrape_url(url)

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

    








