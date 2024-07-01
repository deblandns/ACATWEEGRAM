import sqlite3 as sql

connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

command = f'ALTER TABLE ADMIN ADD COLUMN email VARCHAR(100) NULL'
tweet_data = cursor.execute(command)
# data = tweet_data.fetchall()
# for i in data:
#     if i[2] == True:
#         print("true")
#     else:
#         print("false")
#
