from sql_files import sql_tweet_functions
from datetime import datetime
date_and_time = datetime.now()
instance_for_test = sql_tweet_functions.SqlFunctions(tweet_channel="@dailymonitor", tweet_id="21312", tweet_title="salam", used_comment="working on project", tweet_link="https://x.com/salam/132132132", comment_post_datetime=f"{date_and_time}")
test = instance_for_test.update_data()
print(test)
