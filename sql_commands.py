import sqlite3 as sql

connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

command = f'SELECT tweet_id FROM tweet_data WHERE tweet_channel = "@dailymonitor"'
tweet_data = cursor.execute(command)
data = tweet_data.fetchall()[0][0]
print(data)