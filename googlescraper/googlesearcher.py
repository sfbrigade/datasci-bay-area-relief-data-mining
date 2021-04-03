### usage
# googlesearch.search(str: term, int: num_results=10, str: lang="en") -> list
from googlesearch import search
import requests
import random
class Grants():
    """Google search grants results."""
    def get_search_results(self):
        ### limit language
        A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             )
        Agent = A[random.randrange(len(A))]
        headers = {'User-Agent': Agent}
        url = 'https://www.google.com?q=bay%20area%20covid%20business%20grants'
        # grants = search("bay area covid-19 business grants", num_results=100, lang="en")
        # print(grants)
        # print(len(grants))
        res = requests.get(url, headers=headers)
        return res


