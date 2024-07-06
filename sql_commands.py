import sqlite3 as sql

connect = sql.connect('acatweegram.db')
cursor = connect.cursor()


def run_with_data(user_name):
    command = f"INSERT INTO tweet_data(tweet_channel) VALUES ('{user_name}') "
    tweet_data = cursor.execute(command)
    connect.commit()


run_with_data("@BBCWorld")



