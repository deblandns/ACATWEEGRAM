import datetime
import sqlite3
import sqlite3 as sql
import traceback
import sys

# connect database to project
connect = sql.connect('acatweegram.db')

# set cursor to implement our target sql commands
cursor = connect.cursor()


# this class will do all the sql functions and implement everything we have inside itself
class SqlFunctions:
    def __init__(self, tweet_channel: str = None, tweet_id: str = None, tweet_title: str = None,
                 used_comment: str = None, tweet_link: str = None, comment_post_datetime: datetime.datetime = None):
        """

        this parameter is tweet_channel and must be required but to prevent bugs we don`t implement necessary things:param tweet_channel:
        tweet_id is primary_key of each tweet we can simply find out tweet webpage with this id:param tweet_id:
        the tweet title that show the tweet title user created:param tweet_title:
        we randomly generate it and save it here :param used_comment:
        the tweet link of webpage to admin go and check it:param tweet_link:
        this automatic variable will fill by automatic datetime to find out when did we push our comment to twitter servers:param comment_post_datetime:
        """
        self.tweet_channel = tweet_channel
        self.tweet_id = tweet_id
        self.tweet_title = tweet_title
        self.used_comment = used_comment
        self.tweet_link = tweet_link

    # this function will check new posts and last posts that we checked and if they are different in id it will return True else it will return false
    def Is_tweet_data_equal(self) -> bool:
        """
        just pass the parameters of class and get instance of the class the call this function it`ll automatically return true or false to check new data
        this is tweet id to check is tweet new or not:param tweet_id:
        we need tweet channel to check which channel posted it :param tweet_channel:
        """
        # this variable will run sql command and get tweet_id number from tweet_data database based on channel name
        print(f'this is tweet channel = {self.tweet_channel}')
        get_all_data_equal_to_tweet_channel = cursor.execute(f"SELECT tweet_id FROM tweet_data WHERE tweet_channel = '{self.tweet_channel}' ")
        tweet_sql_id = get_all_data_equal_to_tweet_channel.fetchall()[0][0]
        if tweet_sql_id == self.tweet_id:
            return True
        else:
            return False

    def update_data_or_insert(self) -> bool:
        try:
            comment_post_datetime = datetime.datetime.now()
            command = f"UPDATE tweet_data SET tweet_id = '{self.tweet_id}', tweet_title = '{self.tweet_title}', used_comment = '{self.used_comment}', tweet_link = '{self.tweet_link}' WHERE tweet_channel = '{self.tweet_channel}' "
            cursor.execute(command)
            connect.commit()
            return True
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return False
