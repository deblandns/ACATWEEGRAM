import logging
import sqlite3 as sql
import time
import telegram
import asyncio
import tweepy
import datetime
import requests as re
from telegram import *
from telegram.ext import *
from sql_files.sql_tweet_functions import *
from sql_files.sql_admin_functions import *
from tweepy import *
from comments.comments import *
from tweepy.asynchronous import *
from config import Telegram_config, Accounts
from utilities.email_sender import *
from tweet_functions import get_last_post, comment_post
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
    keyboards = [[
        KeyboardButton(text=f"⚙ settings")], [KeyboardButton(f'🟢 add your desire channel'), KeyboardButton(f"🔴 delete Channel"), KeyboardButton(f'🛢️ check database')]
    ]
    reply_keyboards = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
    # endregion check admin class
    if admin_check_response:
        await context.bot.send_message(update.effective_user.id, f"""\
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
👓 if you want to look at all data inside database click on check_database
🔴 if you want to delete channel click on delete_channel
⚙ if you want to set gmail to get response from or change you data click on settings
""", reply_markup=reply_keyboards)
    else:
        await context.bot.send_message(update.effective_user.id, f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧")


# endregion


# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    # in this section when user click on setting we will send two options like inline keyboards and after that if you send any data it will get
    if "⚙ settings" in update.message.text:
        # send message to page
        keyboards = [[InlineKeyboardButton('add_gmail', callback_data='gmail_add')], [InlineKeyboardButton('change notify method', callback_data="change_notification_method")]]
        reply_keyboards_setting = InlineKeyboardMarkup(keyboards)
        await context.bot.send_message(update.effective_user.id, f"""
if you click on add gmail and you had another gmail 
it will replace but if you don`t have any gmail it will save 📩 
\n 
if you click on change notify method and click on No we don`t send you notification
 in email but if you click on yes we will send you email message but email 
 required otherwise it will get error 🔕 """, reply_markup=reply_keyboards_setting)

    # you can add your desire tweeter user channel to get data from and automatically send comment
    elif "🟢 add your desire channel" in update.message.text:
        await context.bot.send_message(update.effective_user.id, f"""
if you want to add channel to check it also you have to add name of channel starting with "@" so please leave channel name
        """)

    # you can delete your desire channel to prevent sending comment and data
    elif "🔴 delete channel" in update.message.text:
        await context.bot.send_message(update.effective_user.id, f"""
if you want to delete channel that you added please insert the name below

        """)
        # todo: check database channels and insert inside here 👆
    # check database with two options that you can check admin, tweeter_data in your database to find out what happened last time
    elif "🛢️ check database" in update.message.text:
        inline_keyboards = [
            [InlineKeyboardButton('ADMIN DATABASE', callback_data="admin_database_check")], [InlineKeyboardButton("Tweet database", callback_data="tweet_database_check")]
        ]
        markup_keyboard_database = InlineKeyboardMarkup(inline_keyboards)
        await context.bot.send_message(update.effective_user.id, f"""
just click on which database you want to check
        """, reply_markup=markup_keyboard_database)

    # run classes that check for new incoming posts
    instance_Check_post = get_last_post.Check_post(Accounts.accounts, Accounts.accounts_id_ordered)
    instance_Check_post.check_last_post()


# endregion


async def get_user_tweets():
    for user_name, user_id in zip(Accounts.accounts, Accounts.accounts_id_ordered):
        url = "https://twitter154.p.rapidapi.com/user/tweets"

        # parameters that we need to call url with
        querystring = {
            "username": user_name,
            "limit": "1",
            "user_id": user_id,
            "include_replies": False,
            "include_pinned": False
        }

        headers = {
            "x-rapidapi-key": "cb55117503mshb4d680ddb2c3067p1364dejsn60b23ba912e6",
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }

        # # send request by get method and get response
        response = re.get(url, headers=headers, params=querystring)

        # get and extract data from response
        data = response.json()
        tweet_id = data['results'][0]['tweet_id']
        tweet_title = data['results'][0]['text']
        channel_name = data['results'][0]['user']['username']
        random_comment_text = random_comment()
        print(f"random_comment_result {random_comment_text}")

        # in here we will get instance of class sql function and then check the new tweet then run functions
        print(f"this is user name of loop {user_name}")
        # there are instance of sql function to run method of inside it
        check_data_equality = SqlFunctions(tweet_channel=f'{user_name}', tweet_id=f'{tweet_id}')
        is_equal = check_data_equality.Is_tweet_data_equal()
        # this function will get inputs and save them or update them and then send comment
        if is_equal:
            print('data are equal')
            pass
        else:
            try:
                # if data is not equal it mean there are new post so it will send comment and change the row data
                tweet_link = comment_post.send_comment(f'{random_comment_text}', post_id=f'{tweet_id}')
                comment_post_date_time = datetime.datetime.now()
                # make instance of sql functions and save data below it
                sql_update_instance = SqlFunctions(tweet_channel=f'{channel_name}', tweet_id=f'{tweet_id}', tweet_title=f'{tweet_title}', used_comment=f'{random_comment_text}', tweet_link=f"{tweet_link}", comment_post_datetime=f'{comment_post_date_time}')
                save_data = sql_update_instance.update_data()
                # in this section we will run command to send message to all admins about this happening

                # this is instance of function that for each id inside admin table it will send message
                sql_admin_instance = AdminSql()
                data = sql_admin_instance.send_all_admin_ids()
                if save_data:
                    print(f"new row updated from {channel_name} and new dataset has been added")
                    logging.info(msg=f"new row updated from {channel_name} and new dataset has been added")
                else:
                    logging.debug(msg=f"there is problem with adding data to database")
                keyboards = [
                    [InlineKeyboardButton('go to tweet page 🔗', url=tweet_link)],
                    [
                        InlineKeyboardButton('action 1', callback_data="action1"),
                    ]
                ]
                reply_markup_keyboard = InlineKeyboardMarkup(keyboards, )
                for id in data:
                    await bot.send_message(chat_id=f"{id[0]}", text=f"""
Hi user: {id[1]} 🌟 
I`ve sent this message:``{random_comment_text}``\n\n to tweet name: {tweet_title} 😉
                \n
to channel: {user_name}                

and tweet id was: 🔢 {tweet_id}
\n
date & time: {comment_post_date_time}
""", disable_web_page_preview=True, reply_markup=reply_markup_keyboard)
                # if user in it`s setting turn email sending true we can send user notification from email also
                if id[2]:
                    user_email_sending_of_tweets_data(user_name=f"{id[1]}", channel_name=f"{channel_name}", email=f"{id[3]}", random_comment_text=f"{random_comment_text}", tweet_title=f'{tweet_title}', tweet_id=f"{tweet_id}")
                    if user_email_sending_of_tweets_data:
                        await bot.send_message(chat_id=f"{id[0]}", text=f"we`ve sent you the email address because you gave us that permission 📧", disable_web_page_preview=True)
                    else:
                        await bot.send_message(chat_id=f"{id[0]}", text=f"we can`t send you email notification that`s may because you ent us wrong email address")
                else:
                    pass
            except:
                logging.error(msg='can`t send message may it`s repetitive')


# async def run_forever():
#     while True:
#         await get_user_tweets()
#         await asyncio.sleep(1 * 60)  # Adjust the sleep time as needed to control the frequency of the requests
#
#
# # this section will monitoring the data from sources that we need to know about themselves posts and then will comment randomly under their posts
# # after that it will let admin know and send link to admin beside the all data of that posts of pages it should be very fast and avoid spaming a lot
# # because my it block our bot and our services
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run_forever())

async def get_call_back_data(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    await query.answer()
    print(query.data)

# run polling section
app = ApplicationBuilder().token(Telegram_config.token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))
app.add_handler(CallbackQueryHandler(get_call_back_data))

# Start the async task to fetch tweets
if app.run_polling:
    print("working..")
app.run_polling()
