import smtplib as sm


def user_email_sending_for_problem(user_name, channel_name, email, random_comment_text, tweet_title, tweet_id,
                                   telegram_id=None):
    try:
        content = f"""
            Hi user: {user_name} 🌟 
        I`ve sent this message:``{random_comment_text}``\n\n to tweet name: {tweet_title} 😉
                        \n
        to channel: {channel_name}                

        and tweet id was: 🔢 {tweet_id}
            """
        # region send user contactus form for me
        mail = sm.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        sender = 'eshopprojectdiardev@gmail.com'
        recipient = email
        mail.login('eshopprojectdiardev@gmail.com', 'snqrxicwhdulzyfs')
        header = 'To:' + recipient + '\n' + 'From:' \
                 + sender + '\n' + f'subject: {user_name} send the problem\n'
        content = header + content
        mail.sendmail(sender, recipient, content)
        mail.close()
        # endregion
        return True
    except:
        return False
