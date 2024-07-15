import asyncio
import logging
import tweepy
import sqlite3 as sql
import requests as re
from datetime import datetime
from telegram import *
from telegram.ext import *
from comments.comments import random_comment
from tweepy import *
from config import Telegram_config, Accounts
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
client = Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token,
                access_token_secret=access_token_secret)


# region start

# start section in here we save the all codes that will happen when user start the bot and everything in starting handle from here
async def start(update: Update, context: CallbackContext) -> CallbackContext:
    # this variable will get the user id then we will check whether is admin or not
    user_id = update.effective_user.id

    # region check_admin class

    # add last step
    async def update_last_step(userid, message_id):
        try:
            insert_last_step = cursor.execute(
                f"UPDATE ADMIN SET last_stp = 'start_command#{message_id}' WHERE telegram_id = '{userid}' ")
            connect.commit()
            return True
        except:
            return False

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
    # convert simple keys to inline keyboards when user click on /start or start bot
    keyboards = [[InlineKeyboardButton(text=f'add channel 🌐', callback_data=f'add-channel-start-key')],
                 [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")]]
    inline_keyboards = InlineKeyboardMarkup(keyboards)
    # endregion check admin class
    if admin_check:
        admin_greet_message = await context.bot.send_message(update.effective_user.id, f"""\
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
""", reply_markup=inline_keyboards)
        last_step_update = await update_last_step(str(user_id), admin_greet_message['message_id'])
    else:
        await context.bot.send_message(update.effective_user.id,
                                       f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧")


# endregion


# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    # todo: add code to check database first then implement code
    # todo: then add code to see whether the input is prepared command or it`s email then validate it
    message_receive = update.message.text
    if message_receive:
        async def check_last_step(user_id):
            last_step = cursor.execute(f"SELECT last_stp FROM ADMIN WHERE telegram_id = '{user_id}' ")
            last_stp_fetch = last_step.fetchall()
            for data in last_stp_fetch:
                print(data[0])

        user_last_stp_check = await check_last_step(update.effective_user.id)

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
            await bot.send_message(chat_id=update.effective_user.id,
                                   text=f"maybe you are not admin or you don`t have any data please contact this email : hoseinnysyan1385@gmail.com")
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
        for channel_name in list_for_delete:
            print(channel_name[0])


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
    async def remove_channel(channel_name: str) -> bool:
        try:
            command = f"DELETE FROM tweet_data WHERE tweet_channel = '{channel_name}' "
            cursor.execute(command)
            connect.commit()
        except:
            return False

    remove_status = await remove_channel(channel_name)
    await context.bot.send_message(update.effective_user.id, f"Channel '{channel_name}' has been deleted.")
    return ConversationHandler.END


async def set_gmail(update: Update, context: CallbackContext) -> None:
    # Add logic to handle Gmail setting
    user_gmail_name = update.message.text
    if "@" not in user_gmail_name or ".com" not in user_gmail_name or "gmail" not in user_gmail_name:
        await context.bot.send_message(update.effective_user.id,
                                       "you don`t entered email with '@' or .com or 'gmail' please write you email exactly like youremail@gmail.com replace youremail with your email name")
    else:
        user_id = update.effective_user.id

        async def change_gmail(id, gmail):
            try:
                command = f"UPDATE ADMIN SET email = '{gmail}', send_email = TRUE WHERE telegram_id = '{id}' "
                execute = cursor.execute(command)
                connect.commit()
                return True
            except:
                return False

        is_added = await change_gmail(user_id, user_gmail_name)
        if is_added:
            await bot.send_message(update.effective_user.id,
                                   f"your email inserted or changed and we turned email sending on you can turn it off in Email notify 📬 status")
        else:
            await bot.send_message(update.effective_user.id, f"there is problem to set your email to database")
        return
    return ConversationHandler.END


async def call_back_notifications(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'cancell':
        # add last step
        async def update_last_step(userid):
            try:
                insert_last_step = cursor.execute(
                    f"UPDATE ADMIN SET last_stp = 'homepage' WHERE telegram_id = '{userid}' ")
                connect.commit()
                return True
            except:
                return False

        last_step_update = await update_last_step(str(update.effective_user.id))
        if last_step_update:
            await bot.send_message(update.effective_user.id, f"process cancelled")

    if query.data == 'notification_turn_on':
        async def change_notification_status(userid):
            try:
                turn_on_command = f"UPDATE ADMIN SET send_email = TRUE WHERE telegram_id = '{userid}' "
                cursor.execute(turn_on_command)
                connect.commit()
                return True
            except:
                return False

        sending_email_turn_on = await change_notification_status(update.effective_user.id)
        if sending_email_turn_on:
            await context.bot.send_message(update.effective_user.id,
                                           f"your email notification sending status is on you can get notified 🔔")
        else:
            await context.bot.send_message(update.effective_user.id,
                                           f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")

    if query.data == 'notification_off':
        async def TurnOffEmailSending(userid):
            try:
                turn_on_command = f"UPDATE ADMIN SET send_email = FALSE WHERE telegram_id = '{userid}' "
                cursor.execute(turn_on_command)
                connect.commit()
                return True
            except:
                return False

        sending_email_turn_off = await TurnOffEmailSending(update.effective_user.id)
        if sending_email_turn_off:
            await context.bot.send_message(update.effective_user.id, f"email notification sending status is muted 🔇")
        else:
            await context.bot.send_message(update.effective_user.id,
                                           f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")

    if query.data == 'change_email':
        # in there we will change the last step to identify user status
        async def change_email_status(userid, message_id) -> bool:
            try:
                email_ch = cursor.execute(
                    f"UPDATE ADMIN SET last_stp = 'change_email#{message_id}' WHERE telegram_id = '{userid}' ")
                connect.commit()
                return True
            except:
                return False

        edit_email_message = await bot.send_message(chat_id=update.effective_user.id,
                                                    text=f"now insert new email you want to enter \n note: ⚡ it must has '@' sign and end up with '.com' ")
        edit_email = await change_email_status(update.effective_user.id, edit_email_message['message_id'])

    if query.data == 'add_email':
        async def add_email_status(userid, message_id) -> bool:
            try:
                email_ch = cursor.execute(
                    f"UPDATE ADMIN SET last_stp = 'add_email#{message_id}' WHERE telegram_id = '{userid}' ")
                connect.commit()
                return True
            except:
                return False

        add_email_message = await bot.send_message(chat_id=update.effective_user.id,
                                                   text=f"now insert  email you want to enter for the first time 📩 \n note: ⚡ it must has '@' sign and end up with '.com' ")
        add_email = await add_email_status(update.effective_user.id, add_email_message['message_id'])

    if query.data == 'add-channel-start-key':
        # add last step
        async def update_last_step(userid, message_id):
            try:
                insert_last_step = cursor.execute(
                    f"UPDATE ADMIN SET last_stp = 'add_channel#{message_id}' WHERE telegram_id = '{userid}' ")
                connect.commit()
                return True
            except:
                return False

        # get all channels inside the database
        run_get_channel = cursor.execute(f"SELECT tweet_channel FROM tweet_data")
        datas = run_get_channel.fetchall()
        glassy_inline_keyboard_channels = [[], [InlineKeyboardButton(text=f"cancell 🚫", callback_data=f"cancell")]]
        if datas:
            for data in datas:
                glassy_inline_keyboard_channels[0].append(
                    InlineKeyboardButton(text=f"{data[0]}", callback_data=f'{data[0]}'))
            inline_keyboard = InlineKeyboardMarkup(glassy_inline_keyboard_channels)

            # send message to page if database have channel
            add_channel_message = await context.bot.send_message(update.effective_user.id, f"""
                    send us channel name starting with '@' for example: 👉 @example""", reply_markup=inline_keyboard)
            last_step_update = await update_last_step(str(update.effective_user.id), add_channel_message['message_id'])
        else:
            # send message to page if database has no channel
            cancell_button = [[InlineKeyboardButton(text=f"cancell 🚫", callback_data=f"cancell")]]
            rep_cancell_btn = InlineKeyboardMarkup(cancell_button)
            add_channel_message = await context.bot.send_message(update.effective_user.id, f"""
                    send us channel name starting with '@' for example: 👉 @example""", reply_markup=rep_cancell_btn)

    if query.data == 'setting-keyboard-glass-key':
        # add last step
        async def update_last_step(userid, message_id):
            try:
                insert_last_step = cursor.execute(
                    f"UPDATE ADMIN SET last_stp = 'setting#{message_id}' WHERE telegram_id = '{userid}' ")
                connect.commit()
                return True
            except:
                return False

        # in this section we check user email wheter user have email inside database or not
        async def check_user_email(user_id):
            command = cursor.execute(f"SELECT email FROM ADMIN WHERE telegram_id = '{user_id}' ")
            email_data = cursor.fetchall()
            for data in email_data:
                return data[0]

        email = await check_user_email(update.effective_user.id)
        if email:
            inline_keyboards = [[InlineKeyboardButton(text=f"change email📝", callback_data=f"change_email")], [
                InlineKeyboardButton(text=f"notification On 🔔", callback_data=f"notification_turn_on"),
                InlineKeyboardButton(text=f"notification Off 🔕", callback_data=f"notification_off")],
                                [InlineKeyboardButton(text=f"cancell 🚫", callback_data=f"cancell")]]
            reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboards)
            message_with_email = await bot.send_message(update.effective_user.id, f"""
        this is your email: {email}
        do you want to change it or change the notification sending status
                    """, reply_markup=reply_keyboard_markup)
            last_step_update = await update_last_step(str(update.effective_user.id), message_with_email['message_id'])
        else:
            add_email_inline_keyboard = [[InlineKeyboardButton(text=f"add email 📩", callback_data=f"add_email")],
                                         [InlineKeyboardButton(text=f"cancell 🚫", callback_data=f"cancell")]]
            reply_inline_keyboards = InlineKeyboardMarkup(add_email_inline_keyboard)
            message_without_email = await bot.send_message(chat_id=update.effective_user.id,
                                   text=f"please enter your email it must have '@' sign and end with '.com'",
                                   reply_markup=reply_inline_keyboards)
            last_step_update = await update_last_step(str(update.effective_user.id), message_without_email['message_id'])


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
#
#
#         # this function will check new posts and last posts that we checked and if they are different in id it will return True else it will return false
#         async def Is_tweet_data_equal(tweet_channel, tweet_id) -> bool:
#             """
#             just pass the parameters of class and get instance of the class the call this function it`ll automatically return true or false to check new data
#             this is tweet id to check is tweet new or not:param tweet_id:
#             we need tweet channel to check which channel posted it :param tweet_channel:
#             """
#             # this variable will run sql command and get tweet_id number from tweet_data database based on channel name
#             get_all_data_equal_to_tweet_channel = cursor.execute(f"SELECT tweet_id FROM tweet_data WHERE tweet_channel = '{tweet_channel}' ")
#             tweet_sql_id = get_all_data_equal_to_tweet_channel.fetchall()[0][0]
#             if tweet_sql_id == tweet_id:
#                 return True
#             else:
#                 return False
#         is_equal = await Is_tweet_data_equal(f"{user_name}", f"{tweet_id}")
#
#         # this function will get inputs and save them or update them and then send comment
#         if is_equal:
#             print('data are equal')
#             pass
#         else:
#             try:
#                 # if data is not equal it mean there are new post so it will send comment and change the row data
#                 tweet_link = comment_post.send_comment(f'{random_comment_text}', post_id=f'{tweet_id}', channel_name=user_name)
#                 comment_post_date_time = datetime.datetime.now()
#
#                 # this function will update or insert data when is necessary and check the new dataset
#                 async def update_data_or_insert(tweet_channel, tweet_id, tweet_title, used_comment, tweet_link) -> bool:
#                     try:
#                         comment_post_datetime = datetime.datetime.now()
#                         command = f"UPDATE tweet_data SET tweet_id = '{tweet_id}', tweet_title = '{tweet_title}', used_comment = '{used_comment}', tweet_link = '{tweet_link}' WHERE tweet_channel = '{tweet_channel}' "
#                         cursor.execute(command)
#                         connect.commit()
#                         return True
#                     except sqlite3.Error as er:
#                         print('SQLite error: %s' % (' '.join(er.args)))
#                         print("Exception class is: ", er.__class__)
#                         print('SQLite traceback: ')
#                         exc_type, exc_value, exc_tb = sys.exc_info()
#                         print(traceback.format_exception(exc_type, exc_value, exc_tb))
#                         return False
#
#                 save_data = await update_data_or_insert(tweet_channel=f'@{channel_name}', tweet_id=f'{tweet_id}',
#                                                    tweet_title=f'{tweet_title}', used_comment=f'{random_comment_text}',
#                                                    tweet_link=f'{tweet_link}')
#                 async def send_all_admin_ids():
#                     admin_ids = cursor.execute("SELECT telegram_id, name, send_email, email FROM ADMIN")
#                     data = admin_ids.fetchall()
#                     return data
#
#                 data = await send_all_admin_ids()
#
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

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))
app.add_handler(CallbackQueryHandler(call_back_notifications))

# Start the async task to fetch tweets
if app.run_polling:
    print("working..")
app.run_polling()
