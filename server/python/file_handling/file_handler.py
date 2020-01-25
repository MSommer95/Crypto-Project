import os
import time

from server.python.crypto_handling.hash_handler import HashHandler
from server.python.db_handling.db_files import DBfiles
from server.python.file_handling.file_encryptor import FileEncryptor


class FileHandler:

    @staticmethod
    def write_file(user_id, file, file_description):
        file_id = int(round(time.time() * 1000))
        user_path = f'../storage/users/{user_id}'
        size = 0
        path = f'/files/unencrypted/{HashHandler.choose_hash_function("sha1", str(file_id))}'
        with open(f'{user_path}{path}', 'wb') as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)
        DBfiles.insert(file_id, user_id, file.filename, file_description, path, is_encrypted=0)

    @staticmethod
    def change_file_name(user_id, file_id, new_file_name, file_description):
        try:
            DBfiles.update_file(user_id, file_id, new_file_name, file_description)
        except OSError:
            return 'Something went wrong while changing the file'
        else:
            return 'Successfully changed the file'

    @staticmethod
    def delete_file(user_id, file_id, path, is_encrypted):
        try:
            user_path = f'../storage/users/{user_id}'
            os.remove(f'{user_path}{path}')
            if int(is_encrypted):
                FileEncryptor.delete_key(user_id, file_id, user_path)
            DBfiles.delete_file(file_id, user_id)
        except OSError:
            return 'Something went wrong while deleting the file'
        else:
            return 'Successfully deleted the file'
