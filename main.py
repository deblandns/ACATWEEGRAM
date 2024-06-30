import logging
import sqlite3 as sql
import time
import telegram
import asyncio
import tweepy
import requests as re
from telegram import *
from telegram.ext import *
from tweepy import *
from comments.comments import *
from tweepy.asynchronous import *
from config import Telegram_config, Accounts
from tweet_functions.get_last_post import Check_post
from admin_function.check_admin import AdminClass

# the api keys and registration inputs
consumer_key = 'Lrg6mlBu9KMRHwx9C3X0dCiAb'
consumer_secret = 'tAj2K7CO3jZeOgJU0MEyfp9mEECnwV4vnApfnL5UL1oE8R24pZ'
access_token = '1806779267663138816-ABi4RIXEsUSn9E6nU3qrNTutgPQ8Eg'
access_token_secret = "WzvmfTmVWOVGiRjjTMEAGWdvq4wOgH4sw6sg5IkZoaa1y"
bearer_api = "AAAAAAAAAAAAAAAAAAAAALhDugEAAAAAUwaPIWAJJFzIG00CZjaLMR8wahg%3DJ9Ncoe8WNnPxtiEZL2QNKg3KX0TieybMgpZvsFHAtihVTOfwVc"

# Set up logging
# logging.basicConfig(level=logging.INFO)

# config database
connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

# bot is the main api handler for all sources
bot = Bot(token=Telegram_config.token)

# region Twitter config

# Set up Twitter API authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# this is client and it use to authenticate with v2
client = Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret)


# # Verify credentials
# try:
#     api.verify_credentials()
#     print("Authentication OK")
#     available_trends = api.available_trends()
#     print(f"this is hometimeline :{available_trends}")
# except Exception as e:
#     print("Error during authentication", e)
#
#
# # endregion


# region start


# start section in here we save the all codes that will happen when user start the bot and everything in starting handle from here
async def start(update: Update, context: CallbackContext) -> CallbackContext:
    # this variable will get the user id then we will check whether is admin or not
    user_id = update.effective_user.id
    # region check_admin class
    # this class will find out if user is admin or not then response with True or False
    admin_check_instance = AdminClass(user_id)
    admin_check_response = admin_check_instance.check_admin()
    # endregion check admin class
    if admin_check_response:
        await context.bot.send_message(update.effective_user.id, f"Hi Admin 🧨")
    else:
        await context.bot.send_message(update.effective_user.id,
                                       f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧")


# endregion


# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    if "salam" in update.message.text:
        # send message to page
        await context.bot.send_message(update.effective_user.id, f"salam user")
    # run classes that check for new incoming posts
    instance_Check_post = Check_post(Accounts.accounts, Accounts.accounts_id_ordered)
    instance_Check_post.check_last_post()


# endregion

# run polling section
app = ApplicationBuilder().token(Telegram_config.token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))


async def get_user_tweets():
    for user_name, user_id in zip(Accounts.accounts, Accounts.accounts_id_ordered):
        url = "https://twitter154.p.rapidapi.com/user/tweets"

        # parameters that we need to call url with
        querystring = {
            "username": user_name,
            "limit": "1",
            "user_id": user_id,
            "include_replies": "false",
            "include_pinned": "false"
        }

        headers = {
            "x-rapidapi-key": "b2ca57fd49mshcceaec273d8e2a0p143921jsn9a2a5cf40ef4",
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }

        # send request by get method and get response
        response = re.get(url, headers=headers, params=querystring)

        # get and extract data from response
        data = response.json()
        tweet_id = data['results'][0]['tweet_id']
        tweet_title = data['results'][0]['text']
        channel_name = data['results'][0]['user']['username']
        follower_count = data['results'][0]['user']['follower_count']
        media_url = data['results'][0]['media_url']

        # this function should compare the last tweet we got and new tweet

        # query_to_check_database =

        # this function will get inputs and save them or update them
        async def sql_update(tweet_id: int = None, tweet_title: str = None, chennel_name: str = None, follower_count: str = None, media_url: str = None):
            pass


async def run_forever():
    while True:
        await get_user_tweets()
        await asyncio.sleep(1 * 60)  # Adjust the sleep time as needed to control the frequency of the requests


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_forever())

# Start the async task to fetch tweets
if app.run_polling:
    print("working..")
app.run_polling()

# this section will monitoring the data from sources that we need to know about themselves posts and then will comment randomly under their posts
# after that it will let admin know and send link to admin beside the all data of that posts of pages it should be very fast and avoid spaming a lot
# because my it block our bot and our services
