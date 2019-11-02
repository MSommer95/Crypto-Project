from cryptography.fernet import Fernet
from server.python.db_connector import DbConnector
import time


class FileEncryptor:

    @staticmethod
    def file_encryption(user_id, file_id, filename):
        file_id_encrypt = int(round(time.time() * 1000))

        key = Fernet.generate_key()
        key_file_path = '../storage/users/%s/keys/%s.key' % (user_id, filename)
        key_file = open(key_file_path, 'wb')
        key_file.write(key)
        key_file.close()

        db_file = DbConnector.db_get_user_file(file_id, user_id)
        unencrypted_file_path = db_file[0]['path']
        with open(unencrypted_file_path, 'rb') as f:
            data_file = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data_file)
        encrypted_file_path = '../storage/users/%s/files/encrypted/%s.encrypted' % (user_id, filename)
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted)

        is_encrypted = 1
        DbConnector.db_insert_user_file(file_id_encrypt, user_id, filename, encrypted_file_path, is_encrypted)
        DbConnector.db_insert_file_key(user_id, file_id_encrypt, key_file_path)

    @staticmethod
    def file_decryption(user_id, file_id, filename):

        db_file_key = DbConnector.db_get_file_key(file_id, user_id)

        key_file_path = db_file_key[0]['key_path']
        with open(key_file_path, 'rb') as f:
            key = f.read()

        db_file = DbConnector.db_get_user_file(file_id, user_id)

        encrypted_file_path = db_file[0]['path']
        with open(encrypted_file_path, 'rb') as f:
            file = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(file)

        decrypted_file_path = '../storage/users/%s/files/unencrypted/%s' % (user_id, filename)
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted)
