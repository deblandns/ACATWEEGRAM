import sqlite3 as sql

# connect database
connect = sql.connect('acatweegram.db')

# add cursor to do our functions
cursor = connect.cursor()


# this class has three function one for checking email sending status one for turn email sending status on and one for turning it off
class EmailSendingStatus:
    def __init__(self, user_id):
        self.user_id = user_id

    # check now data
    def CheckDataStatus(self):
        try:
            command = f"SELECT * FROM ADMIN WHERE telegram_id = '{self.user_id}' "
            user_data = cursor.execute(command)
            datas = user_data.fetchall()
            return datas
        except:
            return False

    # turn email sending on
    def TurnEmailSendingOn(self):
        try:
            turn_on_command = f"UPDATE ADMIN SET send_email = TRUE WHERE telegram_id = '{self.user_id}' "
            cursor.execute(turn_on_command)
            connect.commit()
            return True
        except:
            return False

    # turn email sending off
    def TurnOffEmailSending(self):
        try:
            turn_on_command = f"UPDATE ADMIN SET send_email = FALSE WHERE telegram_id = '{self.user_id}' "
            cursor.execute(turn_on_command)
            connect.commit()
            return True
        except:
            return False

