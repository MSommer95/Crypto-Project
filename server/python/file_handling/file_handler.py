import os
import time

from server.python.db_handling.db_files import DBfiles


class FileHandler:

    @staticmethod
    def write_file(user_id, file):
        file_id = int(round(time.time() * 1000))
        user_path = '../storage/users/%s' % user_id
        print(type(file))
        size = 0
        path = '/files/unencrypted/%s' % file.filename
        # Write the unencrypted file
        with open(user_path + path, 'wb') as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)

        is_encrypted = 0
        DBfiles.insert(file_id, user_id, file.filename, path, is_encrypted)

    @staticmethod
    def change_file_name(user_id, file_id, new_file_name, old_path, is_encrypted):
        try:
            user_path = '../storage/users/%s' % user_id
            if int(is_encrypted):
                new_path = '/files/encrypted/%s' % new_file_name
                FileHandler.change_key_name(user_id, file_id, new_file_name, user_path)
            else:
                new_path = '/files/unencrypted/%s' % new_file_name

            os.rename(user_path + old_path, user_path + new_path)
        except OSError:
            return 'Something went wrong while changing the file'
        else:
            return 'Successfully changed the file'

    @staticmethod
    def delete_file(user_id, file_id, path, is_encrypted):
        try:
            user_path = '../storage/users/%s' % user_id
            os.remove(user_path + path)
            DBfiles.delete_file(file_id, user_id)
            if int(is_encrypted):
                FileHandler.delete_key(user_id, file_id, user_path)
        except OSError:
            return 'Something went wrong while deleting the file'
        else:
            return 'Successfully deleted the file'

    @staticmethod
    def change_key_name(user_id, file_id, new_file_name, user_path):
        key = DBfiles.get_file_key(file_id, user_id)
        new_path = '/keys/%s' % new_file_name
        try:
            os.rename(user_path + key[0]['key_path'], user_path + new_path)
            DBfiles.update_file_key(key[0]['id'], user_id, file_id, new_path)
        except OSError:
            return 'Something went wrong while changing the key'
        else:
            return 'Successfully changed the key'

    @staticmethod
    def delete_key(user_id, file_id, user_path):
        key = DBfiles.get_file_key(file_id, user_id)
        try:
            os.remove(user_path + key[0]['key_path'])
        except OSError:
            return 'Something went wrong while deleting the key'
        else:
            return 'Successfully deleted the key'
