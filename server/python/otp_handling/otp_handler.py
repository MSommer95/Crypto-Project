# 2FA Funktion nimmt eine user_id und emailadresse entgegen und erstellt einen otp. Anschließend wird dieser an die
# emailadresse geschickt. Der otp wird in der DB gespeichert, zusammen mit einem timestamp
import secrets

from server.python.comm_handling.app_sender import AppSender
from server.python.comm_handling.email_sender import EmailSender
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_otp import DBotp


class OtpHandler:

    @staticmethod
    def create_2fa(user_id):
        otp_value = ''
        for x in range(8):
            otp_value += str(secrets.randbelow(9))
        otp_used = DBotp.check_for_used_otp(user_id, otp_value)

        if otp_used:
            OtpHandler.create_2fa(user_id)
            return
        else:
            DBotp.insert_user_otp(user_id, otp_value)
            return otp_value

    @staticmethod
    def send_otp_mail(otp, email):
        message = 'Your HOTP: %s' % otp
        EmailSender.send_mail(message, '2-Faktor-Auth', email)

    @staticmethod
    def send_otp_app(otp, user_id):
        device = DBdevices.get_active_devices_by_user_id(user_id)
        device_id = device[0]['device_id']
        AppSender.send_otp_to_app(otp, user_id, device_id)