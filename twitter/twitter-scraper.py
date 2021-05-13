import datetime

import requests
import json
import urllib
import csv
import pathlib
import re
import arrow
from typing import Dict, List, Union

# type aliases
data = List[Dict[str, str]]
meta = Dict[str, str]
api_response = Dict[str, Union[data, meta]]
class TwitterScraper:
    def __init__(self) -> None:
        self.set_secrets()
        self.next_token = ''
        self.tweet_dict = set()
    
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
        todays_date_utc = arrow.utcnow()
        one_month_ago = todays_date_utc.shift(months=-1).format('YYYY-MM-DDTHH:mm:ss')
        # formatted_date = datetime.datetime.utcnow().isoformat(timespec=arrow.for)
        # formatted_date = todays_date_utc


        api_base = 'https://api.twitter.com/2/tweets/search/recent?query={}&max_results=50&tweet.fields=created_at'\
            .format(self.query)
        # api_base = 'https://api.twitter.com/2/tweets/search/recent?start_time={formatted_date}&query={query}&max_results=50&tweet.fields=created_at'
        # we only want to add the next token parameter if we need it, otherwise the URL will be invalid

        if self.next_token and len(self.next_token) > 0:
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
        print(r.text)
        r.raise_for_status()
        return r.json()

    def clean_text(self, tweet: Dict[str, str]) -> Dict[str, str]:
        """
        Turns all whitespace in tweets into normal spaces
        """
        text = tweet['text']
        tweet['text'] = re.sub(r'\s+', ' ', text)
        links = re.findall(r'(https:\/\/[^,"\s+]+[^.])', text)

        if tweet['text'] in self.tweet_dict:
            return {}
        else:
            self.tweet_dict.add(tweet['text'])

        if not links:
            return {}

        for link in links:
            if link[-1] == '.':
                links.append(link)

        tweet['links'] = links
        return tweet

    def paginate(self) -> data:
        """
        Makes a series of searches to get all paginated results
        """
        # initial search
        r = self.make_request()
        self.to_csv(r['data'])
        meta = r['meta']
        if 'next_token' in meta:
            self.set_next_token(meta['next_token'] or '')

    def to_csv(self, results: List[Dict[str, str]]) -> None:
        """
        Saves a dict of tweets into a CSV (comma-separated values) with id and text columns
        """
        clean_results = []

        for result in results:
            cleaned_tweet = self.clean_text(result)
            if 'text' in cleaned_tweet:
                clean_results.append(cleaned_tweet)

        with open(self.find_file('tweets.csv'), 'a+') as outfile:
            dw = csv.DictWriter(
                outfile,
                fieldnames=['id', 'text', 'created_at', 'links'],
                delimiter=','
            )
            dw.writerows(clean_results)

    def scrape(self, query: str) -> None:
        """
        Pulls together other functions to actually make and save requests
        """
        self.set_query(query)
        self.paginate()


s = TwitterScraper()
s.scrape('((bay area) OR (san francisco)) small business (grant OR loan OR assistance OR resource)')
# s.scrape('san francisco small business grant')
# Make twitter search call
# Write tweets.csv to a google sheet?
# Data Jam Instructions
# HUMAN: read through spreadsheet, gather relevant table column information, add to official raw data spreadsheet.
# HUMAN: mark loans that have expired as such, 'expired' column
# ROBOT: read from raw data spreadsheet weekly, and add new sources to the database, while removing expired sources.
