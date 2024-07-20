import asyncio
import sys
import logging
import os.path
import random
import smtplib as sm
import sqlite3 as sql
import regex as reg
import requests as re
import pandas as pd
from loguru import logger
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import Update, Bot, InlineKeyboardButton, constants, InlineKeyboardMarkup, User
from telegram.ext import CallbackContext, ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, \
    filters

# region logs
# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logg = logging.getLogger(__name__)
# logger.remove()
# logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")
logger.info('bot started')
# endregion

# region sql config
# config database
file_dir = os.path.dirname('database')
db = os.path.join(file_dir, 'database/acatweegram.db')
connect = sql.connect(db)
cursor = connect.cursor()
# endregion
# region all command extracted

# region random comment
# todo: prevent writing repetitive functions

# todo: add aiosqlite database to project

# todo: read python telegram bot documentation and say them in interview


used_comments = []


async def random_comment() -> str:
    logger.info('random comment generating runned')
    global used_comments
    sql_get_random_comment = cursor.execute("SELECT * FROM comments ORDER BY RANDOM() LIMIT 1")
    picked_comment = sql_get_random_comment.fetchone()
    # used_comments.append(comment_picked)
    return picked_comment[0]


# endregion

# region config
# these are accounts that we will always check them all
# todo: remove account that need to handle manually
accounts = ["@BBCWorld", "@entekhab_news", "@dailymonitor"]
accounts_id_ordered = ['742143', '2682820352', '35697740']

# this is bot token each bot have one of this tokens they use to response each api different
token = '7223989618:AAFQ2Yr9ExJQC58IQwNe-9s8sxiiRqmEPwo'


# endregion

# region get user id based on screen name

# this function will find userid based on channel name its good for validation channels
async def find_channel_id(channel_name):
    try:
        driver = webdriver.Chrome()

        driver.get("https://ilo.so/twitter-id/")

        text_box = driver.find_element(By.ID, "id_username")

        text_box.send_keys(f"{channel_name}")

        text_box.send_keys(Keys.RETURN)

        await asyncio.sleep(3)

        user_id = driver.find_element(By.ID, "user_id").text

        driver.quit()
        if user_id is not None:
            return user_id
    except:
        return False
# endregion

# region send_comment

# this is the function that we call when we want to send comment
url = 'https://x.com/i/api/graphql/oB-5XsHNAbjvARJEc8CZFw/CreateTweet'


async def send_comment(text: str, post_id: str, channel_name: str) -> str:
    logger.info('send comment started')
    """
    add text you want to send as comment and post id you want to send image to
    the channel name that we are going to send message to :param channel_name:
    the text that we are going to send to tweet :param text:
    the post id that we are going to reply comment under it:param post_id:
    this will return link of webpage else it will return false :return:
    """
    # this is cookies when you want to run it on the web and save data on client you can use cookies
    cookies = {
        'auth_token': 'ac02ad63410fdcb83f8b3993f9d2f9582018f120',
        'ct0': 'cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304	',
        'd_prefs': 'MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'des_opt_in': 'Y',
        'dnt': '1',
        'g_state': '{"i_l":0}',
        "guest_id": 'v1%3A172091662864390487',
        'kdt': 'gJHUeGHPIok2rwBLt0h6aTuzJjWN8BpSatvvSqPQ',
        'lang': 'en',
        'night_mode': '2',
        'twid': 'u%3D1806779267663138816'
    }

    # this is header our configs and setting go there
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'Content-Length': '1432',
        'Content-Type': 'application/json',
        'Cookie': 'guest_id=v1%3A172091662864390487; night_mode=2; kdt=gJHUeGHPIok2rwBLt0h6aTuzJjWN8BpSatvvSqPQ; auth_token=ac02ad63410fdcb83f8b3993f9d2f9582018f120; ct0=cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304; twid=u%3D1806779267663138816; lang=en; d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'Origin': 'https://x.com',
        'Priority': 'u=1, i',
        'Referer': f'https://x.com/{channel_name}/status/{post_id}',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Gpc': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Client-Transaction-Id': 'nqXk2313OQNAJsobgR8ri5nPRCIQ4uXKojirRIz5k9NuD6H/qRXdmnYqoeVxSoU0DX672ZxlZmXuifi6Pr91yhi8ps5znQ',
        'X-Client-Uuid': 'b53135cd-091a-41b3-8226-c3d481b926a4',
        'X-Csrf-Token': 'cb0580831790827912a0cf7ad1ae2a6c8a1135aebc340ca60eca18f06f7a28fd654f70585aa3675f8890de9eae0565b7f287243fab23937370979db26007bf14ebe118ca83e2ef86d9fa1e22e12fb304',
        'X-Twitter-Active-User': 'yes',
        'X-Twitter-Auth-Type': 'OAuth2Session',
        'X-Twitter-Client-Language': 'en',
    }

    # this is payload all inputs go there
    payload = {
        "variables": {
            "tweet_text": f"{text}",
            "reply": {
                "in_reply_to_tweet_id": f"{post_id}",
                "exclude_reply_user_ids": []
            },
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "semantic_annotation_ids": []
        },
        "features": {
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "articles_preview_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "oB-5XsHNAbjvARJEc8CZFw"
    }

    # run request and post data to server
    data = re.post(url, json=payload, headers=headers, cookies=cookies)

    # print data to visualize everything we get
    logger.info(f"send comment status code is {data.status_code}")
    logger.info(f"json response from sending comment{data.json()}")
    # this will return post link
    if data.status_code == 200:
        return f"https://x.com/{channel_name}/status/{post_id}"
    else:
        return "not working may you written comment twice"


# endregion


# region email_sender function
def user_email_sending_of_tweets_data(user_name: str = None, channel_name: str = None, email: str = None,
                                      random_comment_text: str = None, tweet_title: str = None, tweet_id: str = None,
                                      telegram_id=None):
    logger.info("email sending function started")
    content = f"""
                Hi user: {user_name} 🌟 
            I`ve sent this message:``{random_comment_text}``\n\n to tweet name: {tweet_title} 😉
                            \n
            to channel: {channel_name}                

            and tweet id was: 🔢 {tweet_id}
                """

    sender = 'eshopprojectdiardev@gmail.com'
    recipient = email

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"{user_name} sent the problem"

    # Attach the message body
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # Send the email
    try:
        with sm.SMTP('smtp.gmail.com', 587) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(sender, 'snqrxicwhdulzyfs')
            mail.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")


# endregion
# endregion

# region sql last_step functions

# region check last step

# get last_step and check it
async def check_last_step(user_id):
    logger.info(f"last step try to check by user id : {user_id}")
    last_step = cursor.execute("SELECT last_stp FROM ADMIN WHERE telegram_id = ? ", (user_id,))
    last_stp_fetch = last_step.fetchone()
    return last_stp_fetch[0]


# endregion

# region start command last_step

# add last step of start
async def update_last_step_start(userid, message_id):
    try:
        message_id_string = f"start_command#{message_id}"
        insert_last_step = cursor.execute("UPDATE ADMIN SET last_stp = ?  WHERE telegram_id = ?",
                                          (message_id_string, userid))
        connect.commit()
        logger.success(f'last step update for user {userid} with message {message_id} started')
        return True
    except:
        logger.warning(f"unable to update last step for user {userid}")
        return False


# endregion

# region update last step to homepage

# region add last step of homepage
async def update_last_step_homepage(userid):
    try:
        insert_last_step = cursor.execute("UPDATE ADMIN SET last_stp = 'homepage' WHERE telegram_id = ?", (userid,))
        connect.commit()
        logger.success(f"last step convert to homepage set for userid {userid}")
        return True
    except:
        logger.warning(f"unable to set step of homepage for userid {userid}")
        return False


# endregion

# region last step to add channel
# add last step add channel
async def update_last_step_add_channel(userid, message_id):
    try:
        add_channel_message_last_step = f'add_channel#{message_id}'
        insert_last_step = cursor.execute(f"UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?",
                                          (add_channel_message_last_step, userid))
        connect.commit()
        return True
    except:
        return False


# endregion

# endregion

# region get all comments
async def get_all_comments():
    get_comments = cursor.execute("SELECT * FROM comments")
    comments = get_comments.fetchall()
    return comments


# endregion

# region update last_stp to add or delete comment
async def add_or_delete_comment(user_id, message_id):
    try:
        f_str_add_del_comm = f"add-delete-comment#{message_id}"
        cursor.execute("UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?", (f_str_add_del_comm, user_id,))
        connect.commit()
        return True
    except:
        return False


# endregion

# region add new comment into a database
async def insert_comment(comment):
    try:
        cursor.execute("INSERT INTO comments VALUES(?)", (comment,))
        connect.commit()
        return True
    except:
        return False


# endregion

# region delete comment based on comment message
async def delete_comment(comment_name):
    try:
        cursor.execute("DELETE FROM comments WHERE comment_title = ?", (comment_name,))
        connect.commit()
        return True
    except:
        return False

# endregion

# endregion

# region bot
# bot is the main api handler for all source
bot = Bot(token=token)


# endregion

# region escape the charectors
# escape the charectors
def escape_characters_for_markdown(text: str):
    result = text.replace(r".", r"\.")
    result = result.replace(r"#", r"\#")
    result = result.replace(r"(", r"\(")
    result = result.replace(r")", r"\)")
    result = result.replace(r"!", r"\!")
    result = result.replace(r"-", r"\-")
    result = result.replace("_", "\_")
    result = result.replace("*", "\*")
    result = result.replace("[", "\[")
    result = result.replace("]", "\]")
    result = result.replace("~", "\~")
    result = result.replace("`", "\`")
    result = result.replace("+", "\+")
    result = result.replace("=", "\=")
    result = result.replace("|", "\|")
    result = result.replace("{", "\{")
    result = result.replace("}", "\}")
    result = result.replace(">", "\>")
    return result
# endregion


# region start
# start section in here we save the all codes that will happen when user start the bot and everything in starting handle from here
async def start(update: Update, context: CallbackContext) -> CallbackContext:
    # this variable will get the user id then we will check whether is admin or not
    user_id = update.effective_user.id
    # log for the user that see which user started the bot
    logger.info(f"userid {user_id} started the bot")

    # region check_admin class
    # check_admin this function name check admin will check the admin and then response True or False base on user_id
    async def check_admin(user_id: int) -> bool:
        """
        this function will get user data from self.user_id then response with True or False
        :return:bool
        """
        admin_data = cursor.execute("SELECT * FROM ADMIN WHERE telegram_id = ?", (user_id,))
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
                 [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")],
                 [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                 [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                 ]
    inline_keyboards = InlineKeyboardMarkup(keyboards)
    # endregion check admin class
    if admin_check:
        logger.success(f"user {user_id} is admin")
        admin_greet_message = await context.bot.send_message(update.effective_user.id,
                                                             text=escape_characters_for_markdown(f"""\
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
click on add comment 🎉 to add or delete comments
"""), reply_markup=inline_keyboards, parse_mode=constants.ParseMode.MARKDOWN_V2)
        last_step_update = await update_last_step_start(str(user_id), admin_greet_message['message_id'])
    else:
        logger.info(f"user f{user_id} is not admin")
        await context.bot.send_message(update.effective_user.id, escape_characters_for_markdown(
            f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧"),
                                       parse_mode=constants.ParseMode.MARKDOWN_V2)
# endregion


# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    message_receive = update.message.text
    logger.info(f"user {update.effective_user.username} inserted {message_receive}")
    if message_receive:
        # run sql command to check last step of user
        user_last_stp_check = await check_last_step(update.effective_user.id)
        try:
            # make last_stp data seperated and set it
            command_split, message_id_split = user_last_stp_check.split('#')
            if command_split == 'add_channel':
                await bot.editMessageText(text=f"please wait while processing...", chat_id=update.effective_user.id,
                                          message_id=message_id_split)
                channel_validate = await find_channel_id(update.message.text)
                # async def channel_validate(channel_name):
                #     if '@' in channel_name:
                #         return True
                #     else:
                #         return False
                #
                # channel_validation = await channel_validate(update.message.text)
                if channel_validate is not False:
                    # insert function below can insert channels that user send to us
                    async def Insert_channel(channel_name):
                        try:
                            run_insertion = cursor.execute("INSERT INTO tweet_data(tweet_channel, tweet_channel_id) VALUES (?, ?)", (channel_name, channel_validate,))
                            connect.commit()
                            return True
                        except:
                            return False
                    insert_data_to_channel = await Insert_channel(update.message.text)
                    if insert_data_to_channel:
                        logger.success(f"user`s new channel name: {message_receive} added to database")
                        # get all channels inside the database
                        run_get_channel = cursor.execute("SELECT tweet_channel FROM tweet_data")
                        datas = run_get_channel.fetchall()
                        glassy_inline_keyboard_channels = [
                            [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
                        if datas:
                            for data in datas:
                                glassy_inline_keyboard_channels.insert(0, [
                                    InlineKeyboardButton(text=f"{data[0]}", callback_data=f'{data[0]}')])
                            inline_keyboards = InlineKeyboardMarkup(glassy_inline_keyboard_channels)
                        await bot.editMessageText(
                            text=f"channel name : {update.message.text} has been added to database ✅",
                            chat_id=update.effective_user.id, message_id=message_id_split,
                            reply_markup=inline_keyboards)
                else:
                    logger.debug(f"user {update.effective_user.username} inserted wrong channel")
                    # this section will edit message and say the issue then change the keys
                    await bot.editMessageText(
                        text=f"wrong format it must be like this @example \n note it must start with '@' sign or you entered channel that doesn`t exist",
                        chat_id=update.effective_user.id, message_id=message_id_split)
                    await asyncio.sleep(3)
                    # get all channels inside the database
                    run_get_channel = cursor.execute(f"SELECT tweet_channel FROM tweet_data")
                    datas = run_get_channel.fetchall()
                    glassy_inline_keyboard_channels = [[InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
                    if datas:
                        for data in datas:
                            glassy_inline_keyboard_channels.insert(0, [
                                InlineKeyboardButton(text=f"{data[0]}", callback_data=f'{data[0]}')])
                        inline_keyboards = InlineKeyboardMarkup(glassy_inline_keyboard_channels)
                    await bot.editMessageText(text=f"please insert channel that you want to auto comment on it",
                                              chat_id=update.effective_user.id, message_id=message_id_split,
                                              reply_markup=inline_keyboards)
            if command_split == 'setting':
                logger.info(f"user trying to send message when user is in setting last step")
                pass
            if command_split == 'change_email':
                async def email_validation(email):
                    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if reg.match(regex, email):
                        return True
                    else:
                        return False

                email_validation_var = await email_validation(update.message.text)
                if email_validation_var:
                    async def change_gmail(id, gmail):
                        try:
                            execute = cursor.execute(
                                "UPDATE ADMIN SET email = ?, send_email = TRUE WHERE telegram_id = ?", (gmail, id,))
                            connect.commit()
                            return True
                        except:
                            return False

                    is_added = await change_gmail(update.effective_user.id, update.message.text)
                    if is_added:
                        logger.success(
                            f"user {update.effective_user.username} with id {update.effective_user.id} inserted new email name {update.message.text} to database")
                        await bot.editMessageText(text=f"your email name: {update.message.text} inserted thanks ❤",
                                                  chat_id=update.effective_user.id, message_id=message_id_split)
                        await asyncio.sleep(3)
                        keyboards = [
                            [InlineKeyboardButton(text=f'add channel 🌐', callback_data=f'add-channel-start-key')],
                            [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")],
                            [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                            [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                        ]
                        inline_keyboards = InlineKeyboardMarkup(keyboards)

                        last_step_update = await update_last_step_homepage(str(update.effective_user.id))
                        await bot.editMessageText(text=f"""
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
""", chat_id=update.effective_user.id, message_id=message_id_split, reply_markup=inline_keyboards)


                else:
                    logger.warning(
                        f"user {update.effective_user.username} has insert the wrong format of email it was: {update.message.text}")
                    await bot.editMessageText(
                        text=f"please enter the right format of email example: \n\n youremail@gmail.com",
                        chat_id=update.effective_user.id, message_id=message_id_split)
                    await asyncio.sleep(7)
                    await bot.editMessageText(text=f"please enter you email address",
                                              chat_id=update.effective_user.id,
                                              message_id=message_id_split)
            if command_split == 'add_email':
                # validation of input
                async def email_validation(email):
                    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if reg.match(regex, email):
                        return True
                    else:
                        return False

                # check the validation
                email_validation_var = await email_validation(update.message.text)
                if email_validation_var:
                    # add email to database of user
                    async def add_email(id, gmail):
                        try:
                            execute = cursor.execute(
                                "UPDATE ADMIN SET email = ?, send_email = TRUE, send_email = TRUE WHERE telegram_id = ?",
                                (gmail, id,))
                            connect.commit()
                            return True
                        except:
                            return False

                    is_added = await add_email(update.effective_user.id, update.message.text)
                    if is_added:
                        logger.success(f"user {update.effective_user.username} inserted it`s first email to database")
                        last_step_update = await update_last_step_homepage(str(update.effective_user.id))
                        inline_keyboards = [
                            [InlineKeyboardButton(text=f"change email📝", callback_data=f"change_email")],
                            [InlineKeyboardButton(
                                text=f"Turn Notification Off 🔕",
                                callback_data=f"notification_off")],
                            [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]
                        ]
                        reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboards)
                        await bot.editMessageText(text=f"email name: {update.message.text} has been added",
                                                  chat_id=update.effective_user.id, message_id=message_id_split,
                                                  reply_markup=reply_keyboard_markup)
                else:
                    logger.debug(f"user {update.effective_user.username} inserted wrong email for the first time")
                    await bot.editMessageText(
                        text=f"your entered wrong email the correct format is 'youremail@gmail.com'\n note: email must have '@' sign and end up with '.com' or other suffixes ",
                        chat_id=update.effective_user.id, message_id=message_id_split)
                    await asyncio.sleep(7)
                    cancell_glass_keyboard = [[InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
                    reply_markup_key = InlineKeyboardMarkup(cancell_glass_keyboard)
                    await bot.editMessageText(text=f"please enter your email address again",
                                              chat_id=update.effective_user.id,
                                              message_id=message_id_split,
                                              reply_markup=reply_markup_key
                                              )
            if command_split == 'add-delete-comment':
                is_insert = await insert_comment(update.message.text)
                if is_insert:
                    await bot.editMessageText(text=f"comment ⚡ {update.message.text} ⚡ has insert to database",
                                              chat_id=update.effective_user.id, message_id=message_id_split)
                    await asyncio.sleep(3)
                    comments = await get_all_comments()
                    inline_keyboards = [[InlineKeyboardButton(f"back ↩", callback_data='cancell')]]
                    for comment in comments:
                        inline_keyboards.insert(0,
                                                [InlineKeyboardButton(f"{comment[0]}", callback_data=f"{comment[0]}")])
                    keyboards = InlineKeyboardMarkup(inline_keyboards)
                    await bot.edit_message_text(
                        text=f"if you want to add comment send it as a message or if you want to delete message exist click on them",
                        chat_id=update.effective_user.id,
                        message_id=message_id_split, reply_markup=keyboards)
            if command_split == 'start_command':
                await bot.send_message(chat_id=update.effective_user.id,
                                       text=f"please click on one of the buttons you want to work with")
            if command_split == 'homepage':
                pass

        except:
            command = user_last_stp_check
            print(command)


# todo: add all queries answer to project
async def call_back_notifications(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    logger.info(f"query data: {query.to_dict()} - {query.data}")
    # check the query to validate whether if query_data is channel name if it`s channel name we will remove it from database
    if query.data:
        # check the query.data if it`s channel or not
        async def channel_validate(channel_name):
            regex = r'@[a-zA-Z0-9.-]'
            if reg.match(regex, channel_name):
                return True
            else:
                return False

        channel_validation = await channel_validate(query.data)
        if channel_validation:
            # Add logic to delete the channel from monitoring
            async def remove_channel(channel_name: str) -> bool:
                try:
                    cursor.execute("DELETE FROM tweet_data WHERE tweet_channel = ?", (channel_name,))
                    connect.commit()
                    return True
                except:
                    return False

            remove_status = await remove_channel(query.data)
            if remove_status:
                await query.answer(text=f"channel name {query.data} has been deleted 💨🕳", show_alert=False)
                # in here we will get last step id to edit message
                user_last_stp_check = await check_last_step(update.effective_user.id)
                last_step_message_id = user_last_stp_check.split('#')[1]
                # edit last message after delete
                # get all channels inside the database
                run_get_channel = cursor.execute(f"SELECT tweet_channel FROM tweet_data")
                datas = run_get_channel.fetchall()
                glassy_inline_keyboard_channels = [[InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
                if datas:
                    for data in datas:
                        glassy_inline_keyboard_channels.insert(0, [
                            InlineKeyboardButton(text=f"{data[0]}", callback_data=f'{data[0]}')])
                    inline_keyboards = InlineKeyboardMarkup(glassy_inline_keyboard_channels)
                await bot.editMessageText(text=f"channel name: {query.data} deleted ⭕",
                                          chat_id=update.effective_user.id, message_id=last_step_message_id,
                                          reply_markup=inline_keyboards)

        last_step_checked = await check_last_step(update.effective_user.id)
        try:
            before_hashtag_comment, after_hashtag_comment = last_step_checked.split('#')
            without_hashtag = None
        except:
            before_hashtag = None
            after_hashtag = None
            without_hashtag = last_step_checked
        # give quick yes or no after user clicked on comment that want
        if before_hashtag_comment == "add-delete-comment":
            if query.data == 'want_delete' or query.data == 'regret_delete_comment':
                pass
            else:
                context.user_data[update.effective_user.id] = query.data
            yes_or_no_glass_keys = [
                [InlineKeyboardButton(text=f"yes 🚮", callback_data=f"want_delete")],
                [InlineKeyboardButton(text=f"no ↩", callback_data=f"regret_delete_comment")]
            ]
            reply_yon_keyboards = InlineKeyboardMarkup(yes_or_no_glass_keys)
            if query.data == 'want_delete' or query.data == 'regret_delete_comment' or query.data == 'cancell':
                pass
            else:
                await bot.editMessageText(text=f"are you sure you want to delete '{query.data}' ",
                                          chat_id=update.effective_user.id, message_id=after_hashtag_comment,
                                          reply_markup=reply_yon_keyboards)
        else:
            pass

    # in here we will remove the exactly comment which user clicked on it based from user cache
    if query.data == 'want_delete':
        logger.success(
            f"data that have to remove is {context.user_data.get(update.effective_user.id)}")  # this will show log of success to continue other process
        user_last_comment_data = context.user_data.get(update.effective_user.id)
        remove_comment = await delete_comment(user_last_comment_data)  # this will delete comment
        if remove_comment:
            logger.success(f"comment {user_last_comment_data} has been deleted")
            comments = await get_all_comments()  # this will get the comments inside database to make it visible for user
            inline_keyboards = [[InlineKeyboardButton(f"back ↩", callback_data='cancell')]]
            for comment in comments:  # for each data inside comment it will add inline keyboard and finally show them all
                inline_keyboards.insert(0, [InlineKeyboardButton(f"{comment[0]}", callback_data=f"{comment[0]}")])
            keyboards = InlineKeyboardMarkup(inline_keyboards)
            user_last_stp_check = await check_last_step(
                update.effective_user.id)  # we will check last step of user and get id of message
            try:
                before_hashtag, after_hashtag = user_last_stp_check.split('#')
                without_hashtag = None
            except:
                before_hashtag = None
                after_hashtag = None
                without_hashtag = user_last_stp_check
            await bot.editMessageText(text=f"comment {user_last_comment_data} has been deleted",
                                      chat_id=update.effective_user.id,
                                      message_id=after_hashtag)
            await asyncio.sleep(3)
            await bot.editMessageText(
                text=f"if you want to add comment send it as a message or if you want to delete message exist click on them",
                chat_id=update.effective_user.id,
                message_id=after_hashtag, reply_markup=keyboards)

    if query.data == 'cancell':
        user_last_stp_check = await check_last_step(update.effective_user.id)
        try:
            before_hashtag, after_hashtag = user_last_stp_check.split('#')
            without_hashtag = None
        except:
            before_hashtag = None
            after_hashtag = None
            without_hashtag = user_last_stp_check

        last_step_update = await update_last_step_homepage(update.effective_user.id)

        if before_hashtag == 'homepage':
            logger.info(f"user redirected from homepage to homepage again")
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=query.message.message_id,
                reply_markup=reply_keyboards)

        if without_hashtag == 'homepage':
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=query.message.message_id,
                reply_markup=reply_keyboards)

        if before_hashtag == 'add_channel':
            logger.info(f'user {update.effective_user.username} cancelled and redirected to homepage from add channel')
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=after_hashtag,
                reply_markup=reply_keyboards)

        if before_hashtag == 'setting':
            logger.info(f'user {update.effective_user.username} cancelled and redirected to homepage from add setting')
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=after_hashtag,
                reply_markup=reply_keyboards)

        if before_hashtag == 'change_email':
            logger.info(
                f'user {update.effective_user.username} cancelled and redirected to homepage from add change email')
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id, message_id=after_hashtag, reply_markup=reply_keyboards)

        if before_hashtag == 'add_email':
            logger.info(
                f'user {update.effective_user.username} cancelled and redirected to homepage from add add email')
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id, message_id=after_hashtag, reply_markup=reply_keyboards)

        # go to homepage if user is inside add-delete-comment section
        if before_hashtag == 'add-delete-comment':
            logger.info(
                f'user {update.effective_user.username} cancelled and redirected to homepage from add add email')
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                                [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id, message_id=after_hashtag, reply_markup=reply_keyboards)

    # this condition will choose True inside database for sending email
    if query.data == 'notification_turn_on':
        logger.success(f"user {update.effective_user.username} changed notification status to on")
        user_last_stp_check = await check_last_step(update.effective_user.id)

        last_stp_message_id = user_last_stp_check.split("#")[1]

        async def change_notification_status(userid):
            try:
                cursor.execute("UPDATE ADMIN SET send_email = TRUE WHERE telegram_id = ?", (userid,))
                connect.commit()
                return True
            except:
                return False

        sending_email_turn_on = await change_notification_status(update.effective_user.id)
        inline_keyboards = [
            [InlineKeyboardButton(text=f"change email📝", callback_data=f"change_email")],
            [InlineKeyboardButton(text=f"Turn notification off 🔕",
                                  callback_data='notification_off')],
            [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]
        ]
        reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboards)
        if sending_email_turn_on:
            logger.success(f"user {update.effective_user.username} successfuly changed the notification status to on")
            await context.bot.editMessageText(text=f"now you can get notified via email 🔔",
                                              chat_id=update.effective_user.id, message_id=last_stp_message_id,
                                              reply_markup=reply_keyboard_markup)
        else:
            logger.warning(f"user {update.effective_user.username} can`t change the email sending notification")
            await context.bot.send_message(update.effective_user.id,
                                           f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")

    if query.data == 'notification_off':
        user_last_stp_check = await check_last_step(update.effective_user.id)

        last_stp_message_id = user_last_stp_check.split("#")[1]

        # turn email sending off
        async def TurnOffEmailSending(userid):
            try:
                cursor.execute("UPDATE ADMIN SET send_email = FALSE WHERE telegram_id = ?", (userid,))
                connect.commit()
                return True
            except:
                return False

        sending_email_turn_off = await TurnOffEmailSending(update.effective_user.id)
        inline_keyboards = [
            [InlineKeyboardButton(text=f"change email📝", callback_data=f"change_email")],
            [InlineKeyboardButton(text=f"Turn notification On 🔔",
                                  callback_data='notification_turn_on')],
            [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]
        ]
        reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboards)
        if sending_email_turn_off:
            logger.success(f"user {update.effective_user.username} changed the notification status to off")
            await context.bot.editMessageText(text=f"now your notification sending status is off 🔕",
                                              chat_id=update.effective_user.id, message_id=last_stp_message_id,
                                              reply_markup=reply_keyboard_markup)
        else:
            logger.warning(f"user {update.effective_user.username} change the notification status to off")
            await context.bot.send_message(update.effective_user.id,
                                           f"may you don`t have any admin account or other problem please contact us via email : hoseinnsyan1385@gmail.com")

    if query.data == 'change_email':
        message_id = query.message.message_id

        # in there we will change the last step to identify user status
        async def change_email_status(userid, message_id) -> bool:
            try:
                message_id_last_Stp = f'change_email#{message_id}'
                email_ch = cursor.execute("UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?",
                                          (message_id_last_Stp, userid))
                connect.commit()
                return True
            except:
                return False

        inline_keyboards = [[InlineKeyboardButton('back ↩', callback_data='cancell')]]
        reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
        edit_email_message = await bot.editMessageText(text=f"insert your new email address 📨",
                                                       chat_id=update.effective_user.id,
                                                       message_id=message_id,
                                                       reply_markup=reply_keyboards
                                                       )
        edit_email = await change_email_status(update.effective_user.id, edit_email_message['message_id'])

    if query.data == 'add_email':
        message_id = query.message.message_id

        async def add_email_status(userid, message_id) -> bool:
            try:
                f_string_message_id = f'add_email#{message_id}'
                email_ch = cursor.execute("UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?",
                                          (f_string_message_id, userid,))
                connect.commit()
                return True
            except:
                return False

        inline_keyboard = [[InlineKeyboardButton(text='back ↩', callback_data='cancell')]]
        reply_keyboards = InlineKeyboardMarkup(inline_keyboard)
        add_email_message = await bot.editMessageText(
            text=f"now insert email you want to enter for the first time 📩 \n note: ⚡ it must has '@' sign and end up with '.com' ",
            chat_id=update.effective_user.id,
            message_id=message_id,
            reply_markup=reply_keyboards)
        add_email = await add_email_status(update.effective_user.id, add_email_message['message_id'])

    if query.data == 'add-channel-start-key':
        logger.info(
            f"user {update.effective_user.username} with id {update.effective_user.id} clicked on add channel key")
        # todo: add query.answer in each of states of functions
        await query.answer(text=f"channels must start with @ sign", show_alert=False)
        message_id = query.message.message_id

        # Get all channels inside the database
        run_get_channel = cursor.execute("SELECT tweet_channel FROM tweet_data")
        datas = run_get_channel.fetchall()
        glassy_inline_keyboard_channels = [[InlineKeyboardButton(text=f"back ↩️", callback_data=f"cancell")]]

        if datas:
            for data in datas:
                # Create a new sublist for each button to display them vertically
                glassy_inline_keyboard_channels.insert(0, [
                    InlineKeyboardButton(text=f"{data[0]}", callback_data=f'{data[0]}')])

            inline_keyboard = InlineKeyboardMarkup(glassy_inline_keyboard_channels)

            # Send message to page if database has channels
            add_channel_message = await context.bot.send_message(
                update.effective_user.id,
                "send us channel name starting with '@' for example: 👉 @example",
                reply_markup=inline_keyboard
            )
            last_step_update = await update_last_step_add_channel(str(update.effective_user.id),
                                                                  add_channel_message['message_id'])
        else:
            # Send message to page if database has no channels
            cancell_button = [[InlineKeyboardButton(text=f"back ↩️", callback_data=f"cancell")]]
            rep_cancell_btn = InlineKeyboardMarkup(cancell_button)
            add_channel_message = await context.bot.send_message(
                update.effective_user.id,
                "send us channel name starting with '@' for example: 👉 @example",
                reply_markup=rep_cancell_btn
            )

    if query.data == 'setting-keyboard-glass-key':
        logger.info(
            f"user {update.effective_user.username} clicked on setting section with user_id {update.effective_user.id} ")

        # add last step
        async def update_last_step_setting(userid, message_id):
            try:
                setting_last_step_change = f'setting#{message_id}'
                insert_last_step = cursor.execute("UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?",
                                                  (setting_last_step_change, userid,))
                connect.commit()
                return True
            except:
                return False

        # in this section we check user email wheter user have email inside database or not
        async def check_user_email(user_id):
            command = cursor.execute("SELECT email, send_email FROM ADMIN WHERE telegram_id = ?", (user_id,))
            email_data = cursor.fetchall()
            for data in email_data:
                return data

        # if we check the user email we based on what we need will send message
        email = await check_user_email(update.effective_user.id)
        if email[0]:
            logger.success(
                f"user {update.effective_user.username} with id {update.effective_user.id} have email inside database")
            inline_keyboards = [
                [InlineKeyboardButton(text=f"change email📝", callback_data=f"change_email")],
                [InlineKeyboardButton(
                    text=f"{'Turn notification On 🔔' if email[1] == 0 else 'Turn notification Off 🔕'}",
                    callback_data=f"{'notification_turn_on' if email[1] == 0 else 'notification_off'}")],
                [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]
            ]
            reply_keyboard_markup = InlineKeyboardMarkup(inline_keyboards)
            message_with_email = await bot.send_message(update.effective_user.id, f"""
        this is your email: {email[0]}
do you want to change it or change the notification sending status
                    """, reply_markup=reply_keyboard_markup)
            last_step_update = await update_last_step_setting(str(update.effective_user.id),
                                                              message_with_email['message_id'])
        else:
            logger.info(
                f"user {update.effective_user.username} with id {update.effective_user.id} has no email so user have to add")
            add_email_inline_keyboard = [[InlineKeyboardButton(text=f"add email 📩", callback_data=f"add_email")],
                                         [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
            reply_inline_keyboards = InlineKeyboardMarkup(add_email_inline_keyboard)
            message_without_email = await bot.send_message(chat_id=update.effective_user.id,
                                                           text=f"please enter your email it must have '@' sign and end with '.com'",
                                                           reply_markup=reply_inline_keyboards)
            last_step_update = await update_last_step_setting(str(update.effective_user.id), ['message_id'])
    # get excel file and send it to user whom want this file to be sended
    if query.data == 'get_excel_file':
        logger.success(
            f"user with userid={update.effective_user.id} want to get excel file {update.effective_user.username}")
        chat_id = update.effective_user.id
        message_id = query.message.message_id
        document_path = os.path.join(os.path.dirname('output.xlsx'), 'output.xlsx')
        await bot.send_document(chat_id=chat_id, document=document_path, caption=f"excel file ☝")
        await bot.editMessageText(text=f"here is your document you can open it with excel opener app 😁",
                                  chat_id=chat_id, message_id=message_id)
        await asyncio.sleep(4)
        keyboards = [[InlineKeyboardButton(text=f'add channel 🌐', callback_data=f'add-channel-start-key')],
                     [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")],
                     [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")],
                     [InlineKeyboardButton(text=f"add comment 🎉", callback_data=f"add-&-delete_comment")]
                     ]
        inline_keyboards = InlineKeyboardMarkup(keyboards)
        await bot.editMessageText(text=f"""
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
""", chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboards)

    if query.data == 'add-&-delete_comment':
        message_id = query.message.message_id
        add_delete_comment = await add_or_delete_comment(update.effective_user.id, message_id)
        # get last message id
        comments = await get_all_comments()  # this will get the comments inside database to make it visible for user
        logger.info(
            f"all of comments are {comments}")  # this log will show the back-end developers about comments  # update last_step of user
        # if user data enter correctly we can add dataset of updates and make a log
        if add_delete_comment:
            logger.success(f"user {update.effective_user.username} updated last stp of add or delete comment")
        else:
            logger.warning(f"user {update.effective_user.username} can not update the last step to add or delete")
        # list of inline keyboards that contain cancel and comments inside database
        inline_keyboards = [[InlineKeyboardButton(f"back ↩", callback_data='cancell')]]
        for comment in comments:
            inline_keyboards.insert(0, [InlineKeyboardButton(f"{comment[0]}", callback_data=f"{comment[0]}")])
        keyboards = InlineKeyboardMarkup(inline_keyboards)
        await bot.edit_message_text(
            text=f"if you want to add comment send it as a message or if you want to delete message exist click on them",
            chat_id=update.effective_user.id,
            message_id=message_id, reply_markup=keyboards)

    if query.data == 'regret_delete_comment':
        # get last message id
        message_id = query.message.message_id
        comments = await get_all_comments()  # this will get the comments inside database to make it visible for user
        logger.info(f"all of comments are {comments}")  # this log will show the back-end developers about comments
        add_delete_comment = await add_or_delete_comment(update.effective_user.id,
                                                         message_id)  # update last_step of user
        # if user data enter correctly we can add dataset of updates and make a log
        if add_delete_comment:
            logger.success(f"user {update.effective_user.username} updated last stp of add or delete comment")
        else:
            logger.warning(f"user {update.effective_user.username} can not update the last step to add or delete")
        # list of inline keyboards that contain cancel and comments inside database
        inline_keyboards = [[InlineKeyboardButton(f"back ↩", callback_data='cancell')]]
        for comment in comments:
            inline_keyboards.insert(0, [InlineKeyboardButton(f"{comment[0]}", callback_data=f"{comment[0]}")])
        keyboards = InlineKeyboardMarkup(inline_keyboards)
        await bot.edit_message_text(
            text=f"if you want to add comment send it as a message or if you want to delete message exist click on them",
            chat_id=update.effective_user.id,
            message_id=message_id, reply_markup=keyboards)


# async def get_user_tweets():
#     for user_name, user_id in zip(accounts, accounts_id_ordered):
#         logger.info(f"bot trying to get this channel {user_name} last tweet")
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
#             "x-rapidapi-key": "b03dbb312fmsh8c93f24c66d3285p103508jsncbe689445f2f",
#             "x-rapidapi-host": "twitter154.p.rapidapi.com"
#         }
#
#         # # send request by get method and get response
#         response = re.get(url, headers=headers, params=querystring)
#
#         # get and extract data from response
#         data = response.json()
#         logger.info(f"api response data {data}")
#         tweet_id = data['results'][0]['tweet_id']
#         tweet_title = data['results'][0]['text']
#         channel_name = data['results'][0]['user']['username']
#         random_comment_text = await random_comment()
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
#             logger.info(f"data is equal so we don`t get any tweet of this channel {user_name} until we get new tweet")
#             pass
#         else:
#             try:
#                 # if data is not equal it mean there are new post so it will send comment and change the row data
#                 tweet_link = await send_comment(f'{random_comment_text}', post_id=f'{tweet_id}', channel_name=user_name)
#
#                 # this function will update or insert data when is necessary and check the new dataset
#                 async def update_data_or_insert(tweet_channel, tweet_id, tweet_title, used_comment, tweet_link) -> bool:
#                     try:
#                         command = f"UPDATE tweet_data SET tweet_id = '{tweet_id}', tweet_title = '{tweet_title}', used_comment = '{used_comment}', tweet_link = '{tweet_link}' WHERE tweet_channel = '{tweet_channel}' "
#                         cursor.execute(command)
#                         connect.commit()
#                         return True
#                     except sql.Error as er:
#                         print('SQLite error: %s' % (' '.join(er.args)))
#                         print("Exception class is: ", er.__class__)
#                         print('SQLite traceback: ')
#                         exc_type, exc_value, exc_tb = sys.exc_info()
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
#                     row = {
#                         'text': [f'{random_comment_text}'],
#                         'link': [f'{tweet_link}'],
#                     }
#                     df = pd.DataFrame(row)
#                     excel_reader = pd.read_excel('output.xlsx')
#                     writer = pd.ExcelWriter('output.xlsx', mode='a', if_sheet_exists='overlay')
#                     df.to_excel(writer, index=False, header=False, startrow=len(excel_reader) + 1)
#                     writer.close()
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
# """, disable_web_page_preview=True, reply_markup=reply_markup_keyboard)
#                 # if user in it`s setting turn email sending true we can send user notification from email also
#                 if id[2]:
#                     user_email_sending_of_tweets_data(user_name=f"{id[1]}", channel_name=f"{channel_name}",
#                                                       email=f"{id[3]}", random_comment_text=f"{random_comment_text}",
#                                                       tweet_title=f'{tweet_title}', tweet_id=f"{tweet_id}")
#                     if user_email_sending_of_tweets_data:
#                         logger.success('email has been send')
#                         await bot.send_message(chat_id=f"{id[0]}",
#                                                text=f"we`ve sent you the email address because you gave us that permission 📧",
#                                                disable_web_page_preview=True)
#                     else:
#                         await bot.send_message(chat_id=f"{id[0]}",
#                                                text=f"we can`t send you email notification that`s may because you ent us wrong email address")
#                 else:
#                     pass
#             except:
#                 logger.critical(f'can`t send message may it`s repetitive inside {user_name}')
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
app = ApplicationBuilder().http_version(http_version='2').token(token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))
app.add_handler(CallbackQueryHandler(call_back_notifications))

# Start the async task to fetch tweets
if app.run_polling:
    logger.success(f"bot is running successfully")
app.run_polling()
