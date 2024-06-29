import tweepy
from tweepy import *

from config import Twitter_config

# region Twitter config

# this authentication is version O.auth 1.0 because we don`t have premium account, and we only can use v2 Twitter api
# config twitter data are set like [consumer_key, consumer_secret, access_token, access_token_secret]
client = Client(
    bearer_token=Twitter_config.bearer_api,
    consumer_key=Twitter_config.consumer_key,
    consumer_secret=Twitter_config.consumer_secret,
    access_token=Twitter_config.access_token,
    access_token_secret=Twitter_config.access_token_secret
)

auth = OAuth1UserHandler(Twitter_config.consumer_key, Twitter_config.consumer_secret, Twitter_config.access_token, Twitter_config.access_token_secret)

api = API(auth)
# endregion


# endregion

# this class will check the last posts on tweeter accounts that we want to fetch data from
class Check_post:
    def __init__(self, screen_name: [], count=1):
        self.screen_name = screen_name
        self.count = count

    def check_last_post(self):
        pass

