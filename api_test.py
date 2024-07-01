from sql_files import sql_tweet_functions

instance_for_test = sql_tweet_functions.SqlFunctions(tweet_channel="@dailymonitor", tweet_id="21312")
test = instance_for_test.Is_tweet_data_equal()
print(test)