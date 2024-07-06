# in this section we will add code to add gmail to our database to get notification from
import sqlite3 as sql

connect = sql.connect("acatweegram.db")

cursor = connect.cursor()


def change_gmail(id, gmail):
    try:
        command = f''
        execute = cursor.execute(command)
        print(execute)
        connect.commit()
        return True
    except:
        return False
