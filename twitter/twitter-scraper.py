import requests
import json
import urllib
import csv
import pathlib
import re
from typing import Dict, List, Union

# type aliases
data = List[Dict[str, str]]
meta = Dict[str, str]
api_response = Dict[str, Union[data, meta]]
class TwitterScraper:
    def __init__(self) -> None:
        self.set_secrets()
        self.next_token = ''
    
    def set_secrets(self) -> None:
        """
        Loads the secrets.json file into a instance variable as a dictionary
        """
        with open(self.find_file('secrets.json')) as file:
            secrets = json.load(file)
            self.secrets = secrets

    def set_query(self, query: str) -> None:
        """
        Sets the current query for searching
        """
        self.query = urllib.parse.quote(query)

    def set_next_token(self, next_token: str) -> None:
        """
        Sets the current next_token for searching
        """
        self.next_token = next_token

    def get_secret(self, secret_key: str) -> str:
        """
        Getter for secret dict
        """
        return self.secrets[secret_key]

    def find_file(self, filename: str) -> str:
        path = pathlib.Path(__file__).parent.absolute()
        return path / filename


    def build_url(self) -> str:
        """
        Interpolate query into Twitter API URL
        """
        api_base = 'https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=created_at'
        # we only want to add the next token parameter if we need it, otherwise the URL will be invalid
        if len(self.next_token) > 0:
            api_base += '&next_token={next_token}'.format(next_token=self.next_token)

        return api_base.format(query=self.query)

    def make_request(self) -> api_response:
        """
        Makes a single GET request to the Twitter API and returns its content as a dictionary
        """
        endpoint = self.build_url()
        bearer_token = 'Bearer {token}'.format(token=self.get_secret('BEARER_TOKEN'))
        headers = { 'Authorization': bearer_token }
        r = requests.get(endpoint, headers=headers)
        # errors for 4xx or 5xx responses
        r.raise_for_status()
        return r.json()

    def clean_text(self, tweet: Dict[str, str]) -> Dict[str, str]:
        """
        Turns all whitespace in tweets into normal spaces
        """
        text = tweet['text']
        tweet['text'] = re.sub(r'\s+', ' ', text)
        return tweet

    def paginate(self) -> data:
        """
        Makes a series of searches to get all paginated results
        """
        # initial search
        r = self.make_request()
        self.to_tsv(r['data'])
        meta = r['meta']
        print(meta)
        self.set_next_token(meta['next_token'] or '')
        # while len(self.next_token) > 0:
        for i in range(3):
            print('Requesting API')
            try:
                r = self.make_request()
                print('Response Recieved -- Saving Results')
                self.to_tsv(r['data'])
                meta = r['meta']
                self.set_next_token(meta['next_token'] or '')
                print('Results Saved')
            except:
                print('Wait a while')

    def to_tsv(self, results: List[Dict[str, str]]) -> None:
        """
        Saves a dict of tweets into a TSV (tab-separated values) with id and text columns
        """
        clean_results = list(map(self.clean_text, results))
        with open(self.find_file('tweets.tsv'), 'a+') as outfile:
            dw = csv.DictWriter(
                outfile,
                fieldnames=['id', 'text', 'created_at'],
                delimiter='\t'
            )
            dw.writerows(clean_results)

    def scrape(self, query: str) -> None:
        """
        Pulls together other functions to actually make and save requests
        """
        self.set_query(query)
        self.paginate()


s = TwitterScraper()
s.scrape('((bay area) OR (san francisco)) small business (grant OR loan OR assistance OR resource) -french')