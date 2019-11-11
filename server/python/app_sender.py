from pyfcm import FCMNotification

from server.python.db_connector import DbConnector


class AppSender:

    @staticmethod
    def send_otp_to_app(otp, user_id):
        devices = DbConnector.db_get_user_devices_by_user_id(user_id)
        api_key_path = '../storage/api_key/api_key'
        with open(api_key_path, 'r') as f:
            api_key = f.read()

        push_service = FCMNotification(api_key=api_key)
        message_title = "OTP-Push"
        message_body = '{otp: "%s", user_id: "%s"}' % (otp, user_id)
        result = push_service.notify_single_device(registration_id=devices[0]['device_id'], message_title=message_title,
                                                   message_body=message_body)
        print(result)
