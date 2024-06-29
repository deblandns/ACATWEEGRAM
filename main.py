import sqlite3 as sql
import telegram
from telegram import *
from telegram.ext import *
from config.config import *
from admin_function.check_admin import AdminClass

# config database
connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

# bot is the main api handler for all sources
bot = Bot(token=token)


# region start

# start section in here we save the all codes that will happen when user start the bot and everything in starting handle from here
async def start(update: Update, context: CallbackContext) -> CallbackContext:
    # this variable will get the user id then we will check whether is admin or not
    user_id = update.effective_user.id
    # region chech_admin class
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


# message the admin that we`ve found new post on twitter
async def CheckPost(update: Update, context: CallbackContext) -> None:

    pass

# run polling section
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler('start', start))
if app.run_polling:
    print("working..")
app.run_polling()
