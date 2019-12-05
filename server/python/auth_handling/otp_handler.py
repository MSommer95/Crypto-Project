# 2FA Funktion nimmt eine user_id und emailadresse entgegen und erstellt einen otp. Anschließend wird dieser an die
# emailadresse geschickt. Der otp wird in der DB gespeichert, zusammen mit einem timestamp
import secrets

from server.python.comm_handling.app_sender import AppSender
from server.python.comm_handling.email_sender import EmailSender
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_otp import DBotp


class OtpHandler:

    # Funktion zum Erstellen eines 8-Stelligen OTP
    @staticmethod
    def create_otp(user_id):
        otp_value = ''
        for x in range(8):
            otp_value += str(secrets.randbelow(9))
        otp_used = DBotp.check_used(user_id, otp_value)

        if otp_used:
            OtpHandler.create_otp(user_id)
            return
        else:
            return otp_value

    # Funktion zum Versenden eines OTPs via Emailadresse
    @staticmethod
    def send_otp_mail(email, otp):
        message = 'Your HOTP: %s' % otp
        EmailSender.send_mail(message, '2-Faktor-Auth', email)

    # Funktion zum Versenden eines OTPs via Push Nachricht
    @staticmethod
    def send_otp_app(user_id, otp):
        device = DBdevices.get_active_devices_by_user_id(user_id)
        device_id = device[0]['device_id']
        AppSender.send_otp_to_app(otp, user_id, device_id)

    @staticmethod
    def prepare_otp_send(user_id, otp_option, user_mail):
        otp = OtpHandler.create_otp(user_id)
        DBotp.insert(user_id, otp)
        if otp_option == 1:
            OtpHandler.send_otp_mail(user_mail, otp)
        elif otp_option == 2:
            OtpHandler.send_otp_app(user_id, otp)
        return 'New OTP send'
