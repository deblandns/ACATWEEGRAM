import asyncio
import logging
from datetime import datetime
import tweepy
import requests as re
from telegram import *
from telegram.ext import *
from comments.comments import random_comment
from database.add_channel import *
from database.remove_channel import *
from tweepy import *
from config import Telegram_config, Accounts
from database.sql_admin_functions import AdminSql
from database.sql_tweet_functions import SqlFunctions
from settings import add_gmail_to_database, change_get_notification_gmail
from tweet_functions import comment_post
from utilities.email_sender import user_email_sending_of_tweets_data

# the api keys and registration inputs
consumer_key = 'Lrg6mlBu9KMRHwx9C3X0dCiAb'
consumer_secret = 'tAj2K7CO3jZeOgJU0MEyfp9mEECnwV4vnApfnL5UL1oE8R24pZ'
access_token = '1806779267663138816-ABi4RIXEsUSn9E6nU3qrNTutgPQ8Eg'
access_token_secret = "WzvmfTmVWOVGiRjjTMEAGWdvq4wOgH4sw6sg5IkZoaa1y"
bearer_api = "AAAAAAAAAAAAAAAAAAAAALhDugEAAAAAUwaPIWAJJFzIG00CZjaLMR8wahg%3DJ9Ncoe8WNnPxtiEZL2QNKg3KX0TieybMgpZvsFHAtihVTOfwVc"

# Set up logging
logging.basicConfig(level=logging.INFO)

# config database
connect = sql.connect('database/acatweegram.db')
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
client = Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

# region start

# Define the conversation states
ADDING_CHANNEL, DELETING_CHANNEL, SETTING_GMAIL = range(3)


# start section in here we save the all codes that will happen when user start the bot and everything in starting handle from here
async def start(update: Update, context: CallbackContext) -> CallbackContext:
    # this variable will get the user id then we will check whether is admin or not
    user_id = update.effective_user.id
    # region check_admin class

    # check_admin this function name check admin will check the admin and then response True or False base on user_id
    async def check_admin(user_id: int) -> bool:
        """
        this function will get user data from self.user_id then response with True or False
        :return:bool
        """
        get_admin_data_sql_command: sql = f"SELECT * FROM ADMIN WHERE telegram_id = '{user_id}' "
        admin_data = cursor.execute(get_admin_data_sql_command)
        for user in admin_data:
            admin_id = user[0]
            if admin_id == str(user_id):
                return True
                return
        else:
            return False

    admin_check = await check_admin(user_id)
    keyboards = [[
        KeyboardButton(text=f"set gmail 📨")], [KeyboardButton(text=f"Email notify 📬 status")],
        [KeyboardButton(f'🟢 add your desire channel'), KeyboardButton(f"🔴 delete Channel")]
    ]
    reply_keyboards = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
    # endregion check admin class
    if admin_check:
        await context.bot.send_message(update.effective_user.id, f"""\
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
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
    if "set gmail 📨" in update.message.text:
        # send message to page
        await context.bot.send_message(update.effective_user.id, f"""
send us your email address for example: 👉 youremail@gmail.com
 """)
        return SETTING_GMAIL

    if "Email notify 📬 status" in update.message.text:
        keyboards = [[InlineKeyboardButton('yes 🟢', callback_data='want_notification')],
                     [InlineKeyboardButton('no 🔴', callback_data="don`t_want_notification")]]
        inline_notification_keyboards = InlineKeyboardMarkup(keyboards)

        # check now data
        async def CheckDataStatus(user_id: str):
            try:
                command = f"SELECT * FROM ADMIN WHERE telegram_id = '{user_id}' "
                user_data = cursor.execute(command)
                datas = user_data.fetchall()
                return datas
            except:
                return False

        data = await CheckDataStatus(str(update.effective_user.id))
        if data:
            pass
        else:
            await bot.send_message(chat_id=update.effective_user.id, text=f"maybe you are not admin or you don`t have any data please contact this email : hoseinnysyan1385@gmail.com")
        await context.bot.send_message(update.effective_user.id, f"""
        if you want to get email notification click on yes 🔔 \n\n if you don`t want to get the notification click on no 🔕
        \n
{'🟩   your email sending status is on we can send you report from email' if data[0][2] == 1 else '🔴   your email sending status is off we don`t send you report from email'}
        """, reply_markup=inline_notification_keyboards)

    # you can add your desire tweeter user channel to get data from and automatically send comment
    elif "🟢 add your desire channel" in update.message.text:
        # this sql function will show reservoired channels
        async def check_database():
            command = f"SELECT tweet_channel FROM tweet_data"
            sql_run = cursor.execute(command)
            fetch = sql_run.fetchall()
            return fetch
        data = await check_database()
        list = []
        for da in data:
            list.append(da)
        await context.bot.send_message(update.effective_user.id, f"""
if you want to add channel to check it also you have to add name of channel starting with "@" so please leave channel name\n\n
now_channels = {list}
        """)
        return ADDING_CHANNEL

    # you can delete your desire channel to prevent sending comment and data
    elif "🔴 delete Channel" in update.message.text:
        # this function will show the channels which are ready to deleter
        async def check_database():
            command = f"SELECT tweet_channel FROM tweet_data"
            sql_run = cursor.execute(command)
            fetch = sql_run.fetchall()
            return fetch
        datas = await check_database()
        list_for_delete = []
        for data in datas:
            list_for_delete.append(data)
        await context.bot.send_message(update.effective_user.id, f"""
if you want to delete channel that you added please insert the name below \n\n
these are now list data = {list_for_delete}
        """)
        return DELETING_CHANNEL


# Handlers for conversation states
async def add_channel(update: Update, context: CallbackContext) -> None:
    channel_name = update.message.text
    if channel_name.startswith('@'):
        # insert function below can insert channels that user send to us
        async def Insert_channel(channel_name):
            try:
                command = f"INSERT INTO tweet_data(tweet_channel) VALUES ('{channel_name}')"
                run_insertion = cursor.execute(command)
                connect.commit()
                return True
            except:
                return False

        insert_data_to_channel = await Insert_channel(channel_name)

        # Process the channel name (e.g., store it, start monitoring it, etc.)
        await context.bot.send_message(update.effective_user.id,
                                       f"Channel '{channel_name}' has been added and will be monitored.")
    else:
        await context.bot.send_message(update.effective_user.id,
                                       "Please provide a valid channel name starting with '@'")
    return ConversationHandler.END


async def delete_channel(update: Update, context: CallbackContext) -> None:
    channel_name = update.message.text
    # Add logic to delete the channel from monitoring
    remove_status = remove_channel(channel_name)
    await context.bot.send_message(update.effective_user.id, f"Channel '{channel_name}' has been deleted.")
    return ConversationHandler.END


async def setting_gmail(update: Update, context: CallbackContext) -> None:
    # Add logic to handle Gmail setting
    user_gmail_name = update.message.text
    if "@" not in user_gmail_name or ".com" not in user_gmail_name or "gmail" not in user_gmail_name:
        await context.bot.send_message(update.effective_user.id,
                                       "you don`t entered email with '@' or .com or 'gmail' please write you email exactly like youremail@gmail.com replace youremail with your email name")
    else:
        user_id = update.effective_user.id
        is_added = add_gmail_to_database.change_gmail(user_id, user_gmail_name)
        if is_added:
            await bot.send_message(update.effective_user.id, f"your email inserted or changed and we turned email sending on you can turn it off in Email notify 📬 status")
        else:
            await bot.send_message(update.effective_user.id, f"there is problem to set your email to database")
        return
    await context.bot.send_message(update.effective_user.id, "Gmail setting updated.")
    return ConversationHandler.END


async def call_back_notifications(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "want_notification":
        email_sending_on_instance = change_get_notification_gmail.EmailSendingStatus(update.effective_user.id)
        sending_email_turn_on = email_sending_on_instance.TurnEmailSendingOn()
        if sending_email_turn_on:
            await context.bot.send_message(update.effective_user.id, f"now you email sending is on and we can send you report message from email")
        else:
            await context.bot.send_message(update.effective_user.id, f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")
    if query.data == "don`t_want_notification":
        email_sending_off_instance = change_get_notification_gmail.EmailSendingStatus(update.effective_user.id)
        sending_email_turn_off = email_sending_off_instance.TurnOffEmailSending()
        if sending_email_turn_off:
            await context.bot.send_message(update.effective_user.id,
                                           f"now we can`t send you report message via email")
        else:
            await context.bot.send_message(update.effective_user.id,
                                           f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")


# Fallback handler in case of an unexpected input
async def cancel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

#
# async def get_user_tweets():
#     for user_name, user_id in zip(Accounts.accounts, Accounts.accounts_id_ordered):
#         url = "https://twitter154.p.rapidapi.com/user/tweets"
#
#         # parameters that we need to call url with
#         querystring = {
#             "username": user_name,
#             "limit": "1",
#             "user_id": user_id,
#             "include_replies": False,
#             "include_pinned": False
#         }
#
#         headers = {
#             "x-rapidapi-key": "cb55117503mshb4d680ddb2c3067p1364dejsn60b23ba912e6",
#             "x-rapidapi-host": "twitter154.p.rapidapi.com"
#         }
#
#         # # send request by get method and get response
#         response = re.get(url, headers=headers, params=querystring)
#
#         # get and extract data from response
#         data = response.json()
#         tweet_id = data['results'][0]['tweet_id']
#         tweet_title = data['results'][0]['text']
#         channel_name = data['results'][0]['user']['username']
#         random_comment_text = random_comment()
#         # in here we will get instance of class sql function and then check the new tweet then run functions
#         # there are instance of sql function to run method of inside it
#         check_data_equality = SqlFunctions(tweet_channel=f'{user_name}', tweet_id=f'{tweet_id}')
#         is_equal = check_data_equality.Is_tweet_data_equal()
#         # this function will get inputs and save them or update them and then send comment
#         if is_equal:
#             print('data are equal')
#             pass
#         else:
#             try:
#                 # if data is not equal it mean there are new post so it will send comment and change the row data
#                 tweet_link = comment_post.send_comment(f'{random_comment_text}', post_id=f'{tweet_id}', channel_name=user_name)
#                 comment_post_date_time = datetime.datetime.now()
#                 # make instance of sql functions and save data below it
#                 # todo: use upsert instead of update in here
#                 sql_update_instance = SqlFunctions(tweet_channel=f'@{channel_name}', tweet_id=f'{tweet_id}',
#                                                    tweet_title=f'{tweet_title}', used_comment=f'{random_comment_text}',
#                                                    tweet_link=f'{tweet_link}')
#                 save_data = sql_update_instance.update_data_or_insert()
#                 # in this section we will run command to send message to all admins about this happening
#
#                 # this is instance of function that for each id inside admin table it will send message
#                 sql_admin_instance = AdminSql()
#                 data = sql_admin_instance.send_all_admin_ids()
#                 if save_data:
#                     logging.info(msg=f"new row updated from {channel_name} and new dataset has been added")
#                 else:
#                     logging.debug(msg=f"there is problem with adding data to database")
#                 keyboards = [
#                     [InlineKeyboardButton('go to tweet page 🔗', url=tweet_link)],
#                 ]
#                 reply_markup_keyboard = InlineKeyboardMarkup(keyboards, )
#                 for id in data:
#                     await bot.send_message(chat_id=f"{id[0]}", text=f"""
# Hi user: {id[1]} 🌟
# I`ve sent this message:``{random_comment_text}``\n\n to tweet name: {tweet_title} 😉
#                 \n
# to channel: {user_name}
#
# and tweet id was: 🔢 {tweet_id}
# \n
# date & time: {comment_post_date_time}
# """, disable_web_page_preview=True, reply_markup=reply_markup_keyboard)
#                 # if user in it`s setting turn email sending true we can send user notification from email also
#                 if id[2]:
#                     user_email_sending_of_tweets_data(user_name=f"{id[1]}", channel_name=f"{channel_name}",
#                                                       email=f"{id[3]}", random_comment_text=f"{random_comment_text}",
#                                                       tweet_title=f'{tweet_title}', tweet_id=f"{tweet_id}")
#                     if user_email_sending_of_tweets_data:
#                         await bot.send_message(chat_id=f"{id[0]}",
#                                                text=f"we`ve sent you the email address because you gave us that permission 📧",
#                                                disable_web_page_preview=True)
#                     else:
#                         await bot.send_message(chat_id=f"{id[0]}",
#                                                text=f"we can`t send you email notification that`s may because you ent us wrong email address")
#                 else:
#                     pass
#             except:
#                 logging.error(msg='can`t send message may it`s repetitive')
#
#
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

# Create the application and pass it your bot's token
app = ApplicationBuilder().token(Telegram_config.token).build()

# Define the conversation handler with the states
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start), MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin)],
    states={
        ADDING_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_channel)],
        DELETING_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_channel)],
        SETTING_GMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, setting_gmail)],
        # todo: add seperated condition for setting gmail and change notify method for each section that we want
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
app.add_handler(CallbackQueryHandler(call_back_notifications))
app.add_handler(conv_handler)

# Start the async task to fetch tweets
if app.run_polling:
    print("working..")
app.run_polling()
