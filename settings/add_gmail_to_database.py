# in this section we will add code to add gmail to our database to get notification from
import sqlite3 as sql

connect = sql.connect("acatweegram.db")

cursor = connect.cursor()


def change_gmail(id, gmail):
    try:
        command = f"UPDATE ADMIN SET email = '{gmail}', send_email = TRUE WHERE telegram_id = '{id}' "
        execute = cursor.execute(command)
        connect.commit()
        return True
    except:
        return False
