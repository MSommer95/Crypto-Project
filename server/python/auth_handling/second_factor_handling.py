from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_users import DBusers


class SecondFactorHandler:

    @staticmethod
    def check_for_second_factor(user_id):
        settings = DBusers.get_user_settings(user_id)
        if settings['2FA-Mail'] == 1 or settings['2FA-Mail'] == 1:
            return True
        else:
            return False

    @staticmethod
    def check_for_active_device(user_id):
        user_devices = DBdevices.get_by_user_id(user_id)
        if not len(user_devices):
            return ''
        for i in range(len(user_devices)):
            if int(user_devices[i]['device_is_active']):
                return 'Active device found. No further action required.'
            elif i == len(user_devices) - 1:
                return SecondFactorHandler.deactivate_device_as_second_factor(user_id)

    @staticmethod
    def activate_device(user_id, device_id):
        DBdevices.set_is_active(user_id, device_id, 1)
        return 'Device activated'

    @staticmethod
    def deactivate_device(user_id, device_id):
        DBdevices.set_is_active(user_id, device_id, 0)
        return 'Device deactivated'

    @staticmethod
    def activate_device_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 1, 0)
        DBusers.set_second_factor_option(user_id, 2, 1)
        return 'Device as second factor activated'

    @staticmethod
    def deactivate_device_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 2, 0)
        if SecondFactorHandler.check_for_second_factor(user_id):
            DBusers.set_second_factor_option(user_id, 1, 1)
            return 'Device as second factor deactivated (Email second factor activated. You can deactivate this too if ' \
                   'you want)'
        else:
            return ''

    @staticmethod
    def activate_email_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 1, 1)
        DBusers.set_second_factor_option(user_id, 2, 0)
        return 'Email as second factor activated (device second factor deactivated)'

    @staticmethod
    def deactivate_email_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 1, 0)
        return 'Email as second factor deactivated (You are now not secured by a second factor)'

    @staticmethod
    def deactivate_both_second_factor_options(user_id):
        DBusers.set_second_factor_option(user_id, 1, 0)
        DBusers.set_second_factor_option(user_id, 2, 0)
        return 'Successfully disabled second factor'
