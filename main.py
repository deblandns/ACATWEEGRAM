import sqlite3 as sql
import telegram
from telegram import *
from telegram.ext import *
from tweepy import *
from config import Telegram_config, Twitter_config, Accounts
from get_last_post.get_last_post import Check_post
from admin_function.check_admin import AdminClass

# config database
connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

# bot is the main api handler for all sources
bot = Bot(token=Telegram_config.token)

# region Twitter config

# this authentication is version O.auth 1.0 because we don`t have premium account, and we only can use v2 Twitter api
# config twitter data are set like [consumer_key, consumer_secret, access_token, access_token_secret]
auth = Client(consumer_key=Twitter_config.config_twitter[0][0], consumer_secret=Twitter_config.config_twitter[0][1], access_token=Twitter_config.config_twitter[1][0], access_token_secret=Twitter_config.config_twitter[1][1])
# this variable will reserve instance of Twitter app function starter
api = API(auth)
# endregion


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
        await context.bot.send_message(update.effective_user.id, f"⚠ Hi you`re not admin dear user if you want to be admin please contact us via gmail: hoseinnysyan1385@gmail.com 📧")
# endregion


# region message_handler
# message the admin that we`ve found new post on Twitter
async def message_admin(update: Update, context: CallbackContext) -> None:
    if "salam" in update.message.text:
        await context.bot.send_message(update.effective_user.id, f"salam user")
    user_id = update.effective_user.id
    instance_Check_post = Check_post(Accounts.accounts[0])
    instance_Check_post.check_last_post()
# endregion

# run polling section
app = ApplicationBuilder().token(Telegram_config.token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_admin))
if app.run_polling:
    print("working..")
app.run_polling()
