# in this section we will represent codes that allow us to create new channel to get response from
import sqlite3 as sql

connect = sql.connect('database/acatweegram.db')

cursor = connect.cursor()


class SqlShowAndInsert:
    def __init__(self, channel_name=None):
        self.channel_name = channel_name

    def check_database(self):
        command = f"SELECT tweet_channel FROM tweet_data"
        sql_run = cursor.execute(command)
        fetch = sql_run.fetchall()
        print(fetch)
        return fetch

    def Insert_channel(self):
        try:
            command = f"INSERT INTO tweet_data(tweet_channel) VALUES ('{self.channel_name}')"
            run_insertion = cursor.execute(command)
            connect.commit()
            return True
        except:
            return False
