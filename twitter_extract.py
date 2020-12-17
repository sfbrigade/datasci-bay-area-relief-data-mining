import tweepy
import preprocessing as p 
import csv
import pandas as pd 
import pprint
import json
from secrets import api_key, api_secret, con_key, con_secret

class TwitterExtract:

    def __init__(self):
        # auth = tweepy.OAuthHandler(con_key, con_secret)
        # auth.set_access_token(api_key, api_secret)

        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(con_key, con_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        self.api = api

    def create_csv(self, tweet_data):
        # tweet_csv = open('tweet_results.csv', 'a')
        df = pd.DataFrame(tweet_data)
        df.to_csv('twitter_grant_data.csv')



    def get_tweets(self):
        api = self.api

        # search_word = '#sf'
        search_words = ['#grant' , '#bayarea', '#sf ']

        # new_search = search_word + " -filter:retweets"

        data = {
            'search_word': [],
            'date_created': [],
            'tweet_id' : [],
            'text' : [],
            'source' : []
        }

        for search_word in search_words:
            for item in tweepy.Cursor(api.search, q=search_word, lang='en').items(10):
                
                json_item = item._json

                data['search_word'].append(search_word)
                data['date_created'].append(json_item['created_at'])
                data['tweet_id'].append(json_item['id'])
                data['text'].append(json_item['text'].encode('utf-8'))
                data['source'].append(json_item['source'])
                # tweet_data = [search_word, json_item['created_at'], json_item['id'], json_item['text'].encode('utf-8'), json_item['source']]
                
                # print('date')
                # print(json_item['created_at'])
                # print('id')
                # print(json_item['id'])
                # print('text')
                # print(json_item['text'])
                # print('source')
                # print(json_item['source'])
                # print(item.entities.get('hashtags'))
        return data

t = TwitterExtract()
tweet_data = t.get_tweets()
t.create_csv(tweet_data)
# pprint.pprint(tweet_data[0])