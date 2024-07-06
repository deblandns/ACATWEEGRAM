import sqlite3 as sql
import datetime


connect = sql.connect('acatweegram.db')
cursor = connect.cursor()


def run_with_data(tweet_id, tweet_title, used_comment, tweet_link, comment_post_datetime, tweet_channel):
    command = f"UPDATE tweet_data SET tweet_id = '{tweet_id}', tweet_title = '{tweet_title}', used_comment = '{used_comment}', tweet_link = '{tweet_link}', comment_post_datetime = '{comment_post_datetime}' WHERE tweet_channel = '{tweet_channel}' "
    tweet_data = cursor.execute(command)
    connect.commit()


comment_post_datetime = datetime.datetime.now()
print(comment_post_datetime)
run_with_data(tweet_id='1809407110150492546', tweet_title='Democrat voters still back Biden – but are open to change', used_comment='test to change everything', tweet_link='https://x.com/BBCWorld/status/1809407110150492546', comment_post_datetime=comment_post_datetime, tweet_channel="@BBCWorld")




