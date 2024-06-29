import tweepy
from tweepy import *
from config import Telegram_config, Twitter_config, Accounts

# region Twitter config

# this authentication is version O.auth 1.0 because we don`t have premium account, and we only can use v2 Twitter api
# config twitter data are set like [consumer_key, consumer_secret, access_token, access_token_secret]
auth = Client(consumer_key=Twitter_config.config_twitter[0][0], consumer_secret=Twitter_config.config_twitter[0][1], access_token=Twitter_config.config_twitter[1][0], access_token_secret=Twitter_config.config_twitter[1][1])
# this variable will reserve instance of Twitter app function starter
api = API(auth)
# endregion


# endregion

# this class will check the last posts on tweeter accounts that we want to fetch data from
class Check_post:
    def __init__(self, screen_name: [], count=1):
        self.screen_name = screen_name
        self.count = count

    def check_last_post(self):
        try:
            print(self.screen_name)
            '''
            this function will see the channels and send_message to admin
            :return: data
            '''
            # get the last Tweet from chanel timeline
            tweets = api.search_tweets
            for tweet in tweets:
                print(f"{tweet.user.name} said: {tweet.full_text}\n")
        except tweepy.TweepyException as e:
            print(f"Error: {e}")
