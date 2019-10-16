# import necessary packages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# create message object instance
class EmailSender:
    @staticmethod
    def send_mail(message, subject, email):
        msg = MIMEMultipart()
        # setup the parameters of the message
        password = "P1MURjXWTAY#e3Ty"
        msg['From'] = "cryptoprojecthshl@gmail.com"
        msg['To'] = email
        msg['Subject'] = subject
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("successfully sent email to %s:" % (msg['To']))
