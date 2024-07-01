import sqlite3 as sql

connect = sql.connect('acatweegram.db')
cursor = connect.cursor()

command = f'INSERT INTO tweet_data(ID, tweet_channel) VALUES (4, "@acatweegram")'
tweet_data = cursor.execute(command)
connect.commit()

