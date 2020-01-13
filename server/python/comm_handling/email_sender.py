import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:

    @staticmethod
    def get_email_key(path):
        with open(path, 'r') as f:
            email_key = f.read()
        return email_key

    @staticmethod
    def create_msg(message, subject, email):
        msg = MIMEMultipart()
        msg['From'] = "cryptoprojecthshl@gmail.com"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        return msg

    @staticmethod
    def send_mail(message, subject, email):
        email_key = EmailSender.get_email_key('../storage/email_key/email_key')
        msg = EmailSender.create_msg(message, subject, email)
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo()
            server_ssl.login(msg['From'], email_key)
            server_ssl.sendmail(msg['From'], msg['To'], msg.as_string())
            server_ssl.close()
            print(f'successfully sent email to {msg["To"]}:')
        except smtplib.SMTPException as e:
            logging.error(e)
