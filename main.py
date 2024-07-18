import asyncio
import sys
import logging
import os.path
import random
import smtplib as sm
import sqlite3 as sql
import regex as reg
import requests as re
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import Update, Bot, InlineKeyboardButton, constants, InlineKeyboardMarkup, User
from telegram.ext import CallbackContext, ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# region logs
# todo: add more accurate and complete logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")
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
global random_comment
# todo: remove this list and get comment from sql with random
# todo: add command to add comment to sql instead of editing message
comments = [
    '👏 Appreciate the detailed report !',
    '📢 Great coverage of the topic !',
    '🌟 This article was very insightful !',
    '👍 Thanks for sharing the news !',
    '📰 Interesting update on current events !'
]

used_comments = []


def random_comment() -> str:
    global comments, used_comments

    # this will Reset the comments list if all have been used
    if len(comments) == 0:
        comments = used_comments[:]
        used_comments = []

    # this variable will Pick a random comment
    comment_picked = random.choice(comments)

    # this section will remove the picked comment from the comments list and add it to the used comments list
    comments.remove(comment_picked)
    used_comments.append(comment_picked)

    return comment_picked


# Example usage
for _ in range(1):  # To see the effect over multiple iterations
    print(random_comment())
# endregion

# region config
# these are accounts that we will always check them all
# todo: remove account that need to handle manually
accounts = ["@BBCWorld", "@entekhab_news", "@dailymonitor"]
accounts_id_ordered = ['742143', '2682820352', '35697740']

# this is bot token each bot have one of this tokens they use to response each api different
token = '7223989618:AAFQ2Yr9ExJQC58IQwNe-9s8sxiiRqmEPwo'
# endregion

# region send_comment
# todo: remove all globals which they are residuals
global send_comment
# this is the function that we call when we want to send comment
url = 'https://x.com/i/api/graphql/oB-5XsHNAbjvARJEc8CZFw/CreateTweet'


def send_comment(text: str, post_id: str, channel_name: str) -> str:
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
    print(data.status_code)
    print(data.json())
    # this will return post link
    if data.status_code == 200:
        return f"https://x.com/{channel_name}/status/{post_id}"
    else:
        return "not working may you written comment twice"


# endregion


# region email_sender function
global user_email_sending_of_tweets_data


def user_email_sending_of_tweets_data(user_name: str = None, channel_name: str = None, email: str = None,
                                      random_comment_text: str = None, tweet_title: str = None, tweet_id: str = None,
                                      telegram_id=None):
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
global check_last_step


# get last_step and check it
async def check_last_step(user_id):
    last_step = cursor.execute("SELECT last_stp FROM ADMIN WHERE telegram_id = ? ", (user_id,))
    last_stp_fetch = last_step.fetchone()
    return last_stp_fetch[0]


# endregion

# region start command last_step
global update_last_step_start


# add last step of start
async def update_last_step_start(userid, message_id):
    try:
        message_id_string = f"start_command#{message_id}"
        insert_last_step = cursor.execute("UPDATE ADMIN SET last_stp = ?  WHERE telegram_id = ?",
                                          (message_id_string, userid))
        connect.commit()
        return True
    except:
        return False


# endregion

# region update last step to homepage
global update_last_step_homepage


# add last step of homepage
async def update_last_step_homepage(userid):
    try:
        insert_last_step = cursor.execute("UPDATE ADMIN SET last_stp = 'homepage' WHERE telegram_id = ?", (userid,))
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
                 [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                 ]
    inline_keyboards = InlineKeyboardMarkup(keyboards)
    # endregion check admin class
    if admin_check:
        admin_greet_message = await context.bot.send_message(update.effective_user.id,
                                                             text=escape_characters_for_markdown(f"""\
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
"""), reply_markup=inline_keyboards, parse_mode=constants.ParseMode.MARKDOWN_V2)
        last_step_update = await update_last_step_start(str(user_id), admin_greet_message['message_id'])
    else:
        await context.bot.send_message(update.effective_user.id, escape_characters_for_markdown(
            f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧"),
                                       parse_mode=constants.ParseMode.MARKDOWN_V2)


# endregion

# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    message_receive = update.message.text
    if message_receive:
        # run sql command to check last step of user
        user_last_stp_check = await check_last_step(update.effective_user.id)
        try:
            # make last_stp data seperated and set it
            command_split, message_id_split = user_last_stp_check.split('#')
            if command_split == 'add_channel':
                async def channel_validate(channel_name):
                    if '@' in channel_name:
                        return True
                    else:
                        return False

                channel_validation = await channel_validate(update.message.text)

                if channel_validation:
                    # insert function below can insert channels that user send to us
                    async def Insert_channel(channel_name):
                        try:
                            run_insertion = cursor.execute("INSERT INTO tweet_data(tweet_channel) VALUES (?)",
                                                           (channel_name,))
                            connect.commit()
                            return True
                        except:
                            return False

                    insert_data_to_channel = await Insert_channel(update.message.text)
                    if insert_data_to_channel:
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
                    # this section will edit message and say the issue then change the keys
                    await bot.editMessageText(
                        text=f"wrong format it must be like this @example \n note it must start with '@' sign",
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
                        await bot.editMessageText(text=f"your email name: {update.message.text} inserted thanks ❤",
                                                  chat_id=update.effective_user.id, message_id=message_id_split)
                        await asyncio.sleep(3)
                        keyboards = [
                            [InlineKeyboardButton(text=f'add channel 🌐', callback_data=f'add-channel-start-key')],
                            [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")],
                            [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                        ]
                        inline_keyboards = InlineKeyboardMarkup(keyboards)

                        last_step_update = await update_last_step_homepage(str(update.effective_user.id))
                        await bot.editMessageText(text=f"""
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
""", chat_id=update.effective_user.id, message_id=message_id_split, reply_markup=inline_keyboards)


                else:
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
            if command_split == 'start_command':
                await bot.send_message(chat_id=update.effective_user.id,
                                       text=f"please click on one of the buttons you want to work with")
            if command_split == 'homepage':
                pass
        except:
            command = user_last_stp_check
            print(command)


async def call_back_notifications(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    print(query.to_dict())
    # await query.answer()
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

    if query.data == 'cancell':
        user_last_stp_check = await check_last_step(update.effective_user.id)
        try:
            before_hashtag, after_hashtag = user_last_stp_check.split('#')
        except:
            without_hashtag = user_last_stp_check

        last_step_update = await update_last_step_homepage(str(update.effective_user.id))

        if before_hashtag == 'add_channel':
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=after_hashtag,
                reply_markup=reply_keyboards)

        if before_hashtag == 'setting':
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id,
                message_id=after_hashtag,
                reply_markup=reply_keyboards)

        if before_hashtag == 'change_email':
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id, message_id=after_hashtag, reply_markup=reply_keyboards)

        if before_hashtag == 'add_email':
            inline_keyboards = [[InlineKeyboardButton(text=f"add channel 🌐", callback_data='add-channel-start-key')],
                                [InlineKeyboardButton(text=f"setting ⚙", callback_data='setting-keyboard-glass-key')],
                                [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                                ]
            reply_keyboards = InlineKeyboardMarkup(inline_keyboards)
            await bot.editMessageText(
                text=f"Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel ⚙️ if you want to set gmail to get response from or change your data click on settings",
                chat_id=update.effective_user.id, message_id=after_hashtag, reply_markup=reply_keyboards)

    if query.data == 'notification_turn_on':
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
            await context.bot.editMessageText(text=f"now you can get notified via email 🔔",
                                              chat_id=update.effective_user.id, message_id=last_stp_message_id,
                                              reply_markup=reply_keyboard_markup)
        else:
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
            await context.bot.editMessageText(text=f"now your notification sending status is off 🔕",
                                              chat_id=update.effective_user.id, message_id=last_stp_message_id,
                                              reply_markup=reply_keyboard_markup)
        else:
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
        # todo: add query.answer in each of states of functions
        await query.answer(text=f"you can add channel", show_alert=True)
        message_id = query.message.message_id

        # add last step
        async def update_last_step_add_channel(userid, message_id):
            try:
                add_channel_message_last_step = f'add_channel#{message_id}'
                insert_last_step = cursor.execute(f"UPDATE ADMIN SET last_stp = ? WHERE telegram_id = ?",
                                                  (add_channel_message_last_step, userid))
                connect.commit()
                return True
            except:
                return False

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
            add_email_inline_keyboard = [[InlineKeyboardButton(text=f"add email 📩", callback_data=f"add_email")],
                                         [InlineKeyboardButton(text=f"back ↩", callback_data=f"cancell")]]
            reply_inline_keyboards = InlineKeyboardMarkup(add_email_inline_keyboard)
            message_without_email = await bot.send_message(chat_id=update.effective_user.id,
                                                           text=f"please enter your email it must have '@' sign and end with '.com'",
                                                           reply_markup=reply_inline_keyboards)
            last_step_update = await update_last_step_setting(str(update.effective_user.id), ['message_id'])
    # get excel file and send it to user whom want this file to be sended
    if query.data == 'get_excel_file':
        chat_id = update.effective_user.id
        message_id = query.message.message_id
        document_path = os.path.join(os.path.dirname('output.xlsx'), 'output.xlsx')
        await bot.send_document(chat_id=chat_id, document=document_path, caption=f"excel file ☝")
        await bot.editMessageText(text=f"here is your document you can open it with excel opener app 😁",
                                  chat_id=chat_id, message_id=message_id)
        await asyncio.sleep(4)
        keyboards = [[InlineKeyboardButton(text=f'add channel 🌐', callback_data=f'add-channel-start-key')],
                     [InlineKeyboardButton(text=f"setting ⚙", callback_data=f"setting-keyboard-glass-key")],
                     [InlineKeyboardButton(text=f"get excel file 📃", callback_data=f"get_excel_file")]
                     ]
        inline_keyboards = InlineKeyboardMarkup(keyboards)
        await bot.editMessageText(text=f"""
Hi Admin 🧨 if you want to add channel to get data from and auto comment click on add_channel 
⚙ if you want to set gmail to get response from or change your data click on settings
and if you want to get comments posted beside their links click on get excel file 📃
""", chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboards)


# async def get_user_tweets():
#     for user_name, user_id in zip(accounts, accounts_id_ordered):
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
#                 tweet_link = send_comment(f'{random_comment_text}', post_id=f'{tweet_id}', channel_name=user_name)
#
#                 # this function will update or insert data when is necessary and check the new dataset
#                 async def update_data_or_insert(tweet_channel, tweet_id, tweet_title, used_comment, tweet_link) -> bool:
#                     try:
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
app = ApplicationBuilder().http_version(http_version='2').token(token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))
app.add_handler(CallbackQueryHandler(call_back_notifications))

# Start the async task to fetch tweets
if app.run_polling:
    print("working..")
app.run_polling()
