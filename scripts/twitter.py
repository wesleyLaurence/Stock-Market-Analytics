"""

    Twitter
    
    This class connects to the Twitter API, and streams tweets relating to companies/stocks,
    then loads tweet meta data into MongoDB Atlas database for further analysis.
    
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler 
from tweepy import Stream
import json
import getpass
from pymongo import MongoClient
from datetime import datetime

# twitter credentials
from .secret import twitter_credentials
tc = twitter_credentials()
ACCESS_TOKEN = tc.access_token
ACCESS_TOKEN_SECRET = tc.access_token_secret
CONSUMER_KEY = tc.consumer_key
CONSUMER_SECRET = tc.consumer_secret

def process_tweet(data):
    
    # extract tweet daya
    tweet_text = data['text']
    time_created = data['created_at']
    user_data = data['user']
    entities = data['entities']
    quote_count = data['quote_count']
    reply_count = data['reply_count']
    favorite_count = data['favorite_count']
    retweet_count = data['retweet_count']

    # parse text into list of words
    words_rough = []
    for word1 in tweet_text.split(' '):
        for word2 in word1.split('\n'):
            words_rough.append(word2) 
   
    # clean each word in list
    words_clean = []
    for word in words_rough:

        # make word lowercase
        word = word.lower()

        # remove unneccesary characters
        char_to_remove = (',','.',';',':',
                          '(',')','!'," ",
                          '"','&','?','!',
                          '\n','|')
        
        for char in char_to_remove:
            word = word.replace(char, " ")

        if " " in word:
            word = word.replace(" ","")

        # disregard blank strings and links
        if (word != "") and ("http" not in word):
            words_clean.append(word) 
        else:
            pass

    dict_data = {"tweet_text"   : tweet_text,
                 "words"        : words_clean,
                 "entities"     : entities,
                 "time_created" : time_created,
                 "author"       : user_data}
        
    return dict_data

all_tweets = []

class TwitterStreamer():
    """
    Class for streaming and processesing live tweets.
    """
    
    def stream_tweets(self, hash_tag_list):
        fetched_tweets_filename = 'tweets.json'
        # This handles Twitter authentication and the connection to the Twitter Streaming AMP
        listener = StdOutListener(fetched_tweets_filename, hash_tag_list[0])
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)  
       
    
class StdOutListener(StreamListener):
    """ This is a basic listener class that just prints received tweets to stdout"""
    
    def __init__(self, fetched_tweets_filename, stock_symbol):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.stock_symbol = stock_symbol
        
        self.password = getpass.getpass('Password: ')
    
    def on_data(self, data):
        
        try:
            data = json.loads(data)
            
            if data['lang'] == 'en':
                
                # prep data for storage
                data = process_tweet(data)

                # connect to MongoDB
                client_connect = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/Twitter?retryWrites=true&w=majority".format(self.password)
                cluster = MongoClient(client_connect)

                # Convert to JSON
                if isinstance(data, dict):
                    data = json.dumps(data)
                else:
                    pass

                # set database and collection
                db = cluster['Stocks']
                collection = db['Twitter']

                now = str(datetime.now()).replace('.','_')
                collection.update_one({"_id" : self.stock_symbol}, {"$set":{now : data}})

            else:
                pass

        except BaseException as e:
            print("Error on data: {}".format(str(e)))
    
    def on_error(self, status):
        print(status)  