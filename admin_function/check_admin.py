import sqlite3 as sql

# config database to this file
connect = sql.connect('acatweegram.db')
cursor = connect.cursor()


# this function will get the user id and response with true or false
class AdminClass:
    def __init__(self, user_id):
        self.user_id = user_id

    # check_admin this function name check admin will check the admin and then response True or False base on user_id
    def check_admin(self) -> bool:
        """
        this function will get user data from self.user_id then response with True or False
        :return:bool
        """
        get_admin_data_sql_command: sql = f"SELECT * FROM ADMIN WHERE telegram_id = '{self.user_id}' "
        admin_data = cursor.execute(get_admin_data_sql_command)
        for user in admin_data:
            admin_id = user[1]
            if admin_id == admin_id:
                return True
                return
        else:
            return False
