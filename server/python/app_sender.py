from pyfcm import FCMNotification

from server.python.db_connector import DbConnector


class AppSender:

    @staticmethod
    def send_otp_to_app(otp, user_id):
        devices = DbConnector.db_get_user_devices_by_user_id(user_id)
        push_service = FCMNotification(api_key="AIzaSyDWUFaqXL_665jxb-j_n65y3OirxVg9gAI")
        message_title = "OTP-Push"
        message_body = "Hey, dein OTP ist ready: %s" % otp
        result = push_service.notify_single_device(registration_id=devices[0]['device_id'], message_title=message_title,
                                                   message_body=message_body)
        print(result)
