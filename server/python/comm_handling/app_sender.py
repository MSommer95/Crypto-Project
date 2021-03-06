from pyfcm import FCMNotification


class AppSender:

    @staticmethod
    def send_otp_to_app(otp, user_id, device_id, auth_token):
        api_key_path = '../storage/api_key/api_key'
        with open(api_key_path, 'r') as f:
            api_key = f.read()

        push_service = FCMNotification(api_key=api_key)
        message_title = "OTP-Push"
        message_body = f'{{otp: "{otp}", user_id: "{user_id}", auth_token: "{auth_token}"}}'
        result = push_service.notify_single_device(registration_id=device_id, message_title=message_title,
                                                   message_body=message_body)
        print(result)
