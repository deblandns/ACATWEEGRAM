import sqlite3 as sql
# in this section we will add function which it can remove channel from our database and list

# this function will remove the channel user give us
connect = sql.connect("database/acatweegram.db")

cursor = connect.cursor()


def remove_channel(channel_name: str) -> bool:
    try:
        command = f"DELETE FROM tweet_data WHERE tweet_channel = '{channel_name}' "
        cursor.execute(command)
        connect.commit()
    except:
        return False
