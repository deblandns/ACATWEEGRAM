import smtplib as sm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def user_email_sending_for_problem(user_name: str = None, channel_name: str = None, email: str = None,
                                   random_comment_text: str = None, tweet_title: str = None, tweet_id: str = None,
                                   telegram_id=None):
    content = f"""
                Hi user: {user_name} 🌟 
            I`ve sent this message:``{random_comment_text}``\n\n to tweet name: {tweet_title} 😉
                            \n
            to channel: {channel_name}                

            and tweet id was: 🔢 {tweet_id}
                """

    sender = 'eshopprojectdiardev@gmail.com'
    recipient = email

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"{user_name} sent the problem"

    # Attach the message body
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # Send the email
    try:
        with sm.SMTP('smtp.gmail.com', 587) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(sender, 'snqrxicwhdulzyfs')
            mail.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
