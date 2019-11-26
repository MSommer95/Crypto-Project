from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_users import DBusers


class SecondFactorHandler:

    @staticmethod
    def check_for_active_device(user_id):
        user_devices = DBdevices.get_devices_by_user_id(user_id)
        for i in range(len(user_devices)):
            if int(user_devices[i]['device_is_active']):
                return 'Active device found. No further action required.'
            elif i == len(user_devices) - 1:
                return SecondFactorHandler.deactivate_device_as_second_factor(user_id)

    @staticmethod
    def activate_device(user_id, device_id):
        DBdevices.set_active_user_device(user_id, device_id, 1)
        return 'Device activated'

    @staticmethod
    def deactivate_device(user_id, device_id):
        DBdevices.set_active_user_device(user_id, device_id, 0)
        return 'Device deactivated'

    @staticmethod
    def deactivate_device_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 2, 0)
        DBusers.set_second_factor_option(user_id, 1, 1)
        return 'Device as second factor deactivated (Email second factor activated. You can deactivate this too if ' \
               'you want)'

    @staticmethod
    def activate_email_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 1, 1)
        DBusers.set_second_factor_option(user_id, 2, 0)
        return 'Email as second factor activated (device second factor deactivated)'

    @staticmethod
    def deactivate_email_as_second_factor(user_id):
        DBusers.set_second_factor_option(user_id, 1, 0)
        return 'Email as second factor deactivated (You are now not secured by a second factor)'
