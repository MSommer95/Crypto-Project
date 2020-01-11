import os
import time

from cryptography.fernet import Fernet

from server.python.crypto_handler.hash_handler import HashHandler
from server.python.db_handling.db_files import DBfiles


class FileEncryptor:

    @staticmethod
    def create_key(user_path, key_file_path):
        key = Fernet.generate_key()
        key_file = open(f'{user_path}{key_file_path}', 'wb')
        key_file.write(key)
        key_file.close()
        return key

    @staticmethod
    def get_key(user_id, file_id, user_path):
        db_file_key = DBfiles.get_file_key(file_id, user_id)
        key_file_path = db_file_key[0]['key_path']
        with open(f'{user_path}{key_file_path}', 'rb') as f:
            key = f.read()
        return key

    @staticmethod
    def delete_key(user_id, file_id, user_path):
        key = DBfiles.get_file_key(file_id, user_id)
        try:
            os.remove(f'{user_path}{key[0]["key_path"]}')
        except OSError:
            return 'Something went wrong while deleting the key'
        else:
            return 'Successfully deleted the key'

    @staticmethod
    def prepare_for_crypt(file_id, user_id, user_path):
        db_file = DBfiles.get_file(file_id, user_id)
        unencrypted_file_path = db_file[0]['path']
        file_name = db_file[0]['file_name']
        with open(f'{user_path}{unencrypted_file_path}', 'rb') as f:
            file_data = f.read()
        return file_data, file_name

    # Funktion zum Verschlüsseln einer Datei
    @staticmethod
    def encrypt(user_id, file_id):
        try:
            multi_id = int(round(time.time() * 1000))
            user_path = f'../storage/users/{user_id}'
            key_file_path = f'/keys/{HashHandler.choose_hash_function("sha1", str(multi_id + 1))}.key'
            key = FileEncryptor.create_key(user_path, key_file_path)
            file_data, file_name = FileEncryptor.prepare_for_crypt(file_id, user_id, user_path)
            fernet = Fernet(key)
            encrypted_file = fernet.encrypt(file_data)
            encrypted_filename = f'{file_name}.encrypted'
            encrypted_file_path = f'/files/encrypted/{HashHandler.choose_hash_function("sha1", str(multi_id))}'
            with open(user_path + encrypted_file_path, 'wb') as f:
                f.write(encrypted_file)
            file_description = 'My encrypted file'
            DBfiles.insert(multi_id, user_id, encrypted_filename, file_description, encrypted_file_path,
                           is_encrypted=1)
            DBfiles.insert_file_key(user_id, multi_id, key_file_path, multi_id + 1)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while encrypting the file'
        else:
            return 'Successfully encrypted the file'

    # Funktion zum Entschlüsseln einer Datei
    @staticmethod
    def decrypt(user_id, file_id):
        try:
            file_id_decrypt = int(round(time.time() * 1000))
            user_path = f'../storage/users/{user_id}'
            key = FileEncryptor.get_key(user_id, file_id, user_path)
            file, file_name = FileEncryptor.prepare_for_crypt(file_id, user_id, user_path)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(file)
            decrypted_file_path = f'/files/unencrypted/{HashHandler.choose_hash_function("sha1", str(file_id_decrypt))}'
            with open(f'{user_path}{decrypted_file_path}', 'wb') as f:
                f.write(decrypted)
            file_description = 'My decrypted file'
            DBfiles.insert(file_id_decrypt, user_id, file_name.replace('.encrypted', ''), file_description,
                           decrypted_file_path, is_encrypted=0)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while decrypting the file'
        else:
            return 'Successfully decrypted the file'
