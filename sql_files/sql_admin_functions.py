import sqlite3 as sql

connect = sql.connect('acatweegram.db')

cursor = connect.cursor()


class AdminSql:
    def __init__(self):
        pass

    def send_all_admin_ids(self):
        admin_ids = cursor.execute("SELECT telegram_id, name FROM ADMIN")
        data = admin_ids.fetchall()
        return data


instance_test = AdminSql()
instance_test.send_all_admin_ids()
