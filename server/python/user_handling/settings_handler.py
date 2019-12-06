from server.python.auth_handling.hash_handler import HashHandler
from server.python.auth_handling.second_factor_handling import SecondFactorHandler
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_users import DBusers


class SettingsHandler:

    @staticmethod
    def prepare_user_settings(user_id):
        user_settings = DBusers.get_user_settings(user_id)
        user = DBusers.get_user(user_id)
        user_settings['email'] = user[0]['email']
        return user_settings

    @staticmethod
    def update_account_info(user_id, user_mail, email, password, old_password):
        email_change_status = ''
        password_change_status = ''
        if not user_mail == email:
            email_change_status = DBusers.update_email(user_id, email)
        if not password == '':
            if SettingsHandler.varify_old_password(user_id, old_password):
                if not password == old_password:
                    password_change_status = DBusers.update_password(user_id, password)
                else:
                    password_change_status = 'Please dont use your old password'
            else:
                password_change_status = 'Old password was wrong.'
        return email_change_status + password_change_status

    @staticmethod
    def change_second_factor_options(sec_fa_email, sec_fa_app, user_id):
        if sec_fa_app == 'true':
            devices = DBdevices.get_by_user_id(user_id)
            if len(devices) == 0:
                return 'No active device found! Do you want to register one?'
        if sec_fa_email == 'true':
            SecondFactorHandler.activate_email_as_second_factor(user_id)
        elif sec_fa_app == 'true':
            SecondFactorHandler.activate_device_as_second_factor(user_id)
        token = HashHandler.create_token(user_id, 1)
        return 'Successfully changed the second factor, use token: "%s" to reset your 2FA settings ' % token

    @staticmethod
    def check_second_factor_options(sec_fa, sec_fa_email, sec_fa_app, user_id):
        if sec_fa_email == 'true' and sec_fa_app == 'true':
            return 'Please dont try to check more then one 2FA option'
        else:
            if sec_fa == 'true':
                return SettingsHandler.change_second_factor_options(sec_fa_email, sec_fa_app, user_id)
            else:
                return SecondFactorHandler.deactivate_both_second_factor_options(user_id)

    @staticmethod
    def varify_old_password(user_id, old_password):
        db_old_password = DBusers.get_password(user_id)[0]['password']
        return HashHandler.verify_password(db_old_password, old_password)
