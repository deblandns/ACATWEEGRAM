import sqlite3 as sql
import datetime


connect = sql.connect('database/acatweegram.db')
cursor = connect.cursor()


def run_with_data():
    command = f"INSERT INTO tweet_data(tweet_channel) VALUES('@dailymonitor')"
    tweet_data = cursor.execute(command)
    connect.commit()

run_with_data()


