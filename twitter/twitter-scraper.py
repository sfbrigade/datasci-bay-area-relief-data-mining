import requests
import json
import csv
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
        with open('secrets.json') as file:
            secrets = json.load(file)
            self.secrets = secrets

    def set_query(self, query: str) -> None:
        """
        Sets the current query for searching
        """
        self.query = query

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

    def build_url(self) -> str:
        """
        Interpolate query into Twitter API URL
        """
        api_base = 'https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100'
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

    def paginate(self, query: str):
        """
        Makes a series of searches to get all paginated results
        """
        # initial search
        self.set_query(query)
        r = self.make_request()
        results = r['data']
        meta = r['meta']
        self.set_next_token(meta['next_token'] or '')

        



s = TwitterScraper()
print(s.paginate('meme'))
