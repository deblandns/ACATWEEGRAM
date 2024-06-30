import tweepy
from tweepy import *
from tweepy.asynchronous import *


# the api keys and registration inputs
consumer_key = 'Lrg6mlBu9KMRHwx9C3X0dCiAb'
consumer_secret = 'tAj2K7CO3jZeOgJU0MEyfp9mEECnwV4vnApfnL5UL1oE8R24pZ'
access_token = '1806779267663138816-ABi4RIXEsUSn9E6nU3qrNTutgPQ8Eg'
access_token_secret = "WzvmfTmVWOVGiRjjTMEAGWdvq4wOgH4sw6sg5IkZoaa1y"
bearer_api = "AAAAAAAAAAAAAAAAAAAAALhDugEAAAAA%2FgGoqbnw9nkQpMgPR0un%2B6dAK6A%3DxtnYoYs6kJ434gDbwt1h1YMu0GzF1ucgfH8sIUGpXLy3nPXuBT"


# region Twitter config

# this authentication is version O.auth 1.0 because we don`t have premium account, and we only can use v2 Twitter api
# config twitter data are set like [consumer_key, consumer_secret, access_token, access_token_secret]
client = Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)

api = API(auth)
# endregion


# endregion

# this class will check the last posts on tweeter accounts that we want to fetch data from
class Check_post:
    def __init__(self, screen_name: [], screen_names_id: [], count=1):
        self.screen_name = screen_name
        self.screen_name_id = screen_names_id
        self.count = count

    def check_last_post(self):
        pass


