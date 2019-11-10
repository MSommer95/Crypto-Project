# 2FA Funktion nimmt eine user_id und emailadresse entgegen und erstellt einen otp. Anschließend wird dieser an die
# emailadresse geschickt. Der otp wird in der DB gespeichert, zusammen mit einem timestamp
import secrets

from server.python.app_sender import AppSender
from server.python.db_connector import DbConnector
from server.python.email_sender import EmailSender


class OtpHandler:

    @staticmethod
    def create_2fa(user_id):
        otp_value = ''
        for x in range(8):
            otp_value += str(secrets.randbelow(9))
        otp_used = DbConnector.db_check_for_used_otp(user_id, otp_value)

        if otp_used:
            OtpHandler.create_2fa(user_id)
            return
        else:
            DbConnector.db_insert_user_2fa(user_id, otp_value)
            return otp_value

    @staticmethod
    def send_otp_mail(otp, email):
        message = 'Your HOTP: %s' % otp
        EmailSender.send_mail(message, '2-Faktor-Auth', email)

    @staticmethod
    def send_otp_app(otp, user_id):
        AppSender.send_otp_to_app(otp, user_id)
