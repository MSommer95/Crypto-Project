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
        DBfiles.db_insert_user_file(file_id, user_id, file.filename, path, is_encrypted)

    @staticmethod
    def change_file_name(user_id, new_file_name, old_path, is_encrypted):
        try:
            user_path = '../storage/users/%s' % user_id
            if int(is_encrypted):
                new_path = '/files/encrypted/%s' % new_file_name
            else:
                new_path = '/files/unencrypted/%s' % new_file_name

            os.rename(user_path + old_path, user_path + new_path)
        except OSError:
            return 'Something went wrong'
        else:
            return 'Success'
