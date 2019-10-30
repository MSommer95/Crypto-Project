
# 2FA Funktion nimmt eine user_id und emailadresse entgegen und erstellt einen otp. Anschließend wird dieser an die
# emailadresse geschickt. Der otp wird in der DB gespeichert, zusammen mit einem timestamp
import secrets

from server.python.db_connector import DbConnector
from server.python.email_sender import EmailSender


class OtpHandler:

    @staticmethod
    def create_2FA(user_id, email):
        otp_value = ''
        for x in range(8):
            otp_value += str(secrets.randbelow(9))
        db = DbConnector.create_db_connection()
        otp_used = DbConnector.check_for_used_otp(db, user_id, otp_value)

        if otp_used:
            OtpHandler.create_2FA(user_id, email)
            return
        else:
            db = DbConnector.create_db_connection()
            DbConnector.update_user_2fa(db, user_id, otp_value)
            return otp_value

    @staticmethod
    def send_otp_mail(otp, email):
        message = 'Your HOTP: %s' % otp
        EmailSender.send_mail(message, '2-Faktor-Auth', email)

    @staticmethod
    def send_otp_app(otp, params):
        # TODO send otp to app
        return
