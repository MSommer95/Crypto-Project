import time

from cryptography.fernet import Fernet

from server.python.db_handling.db_files import DBfiles


class FileEncryptor:

    @staticmethod
    def encryption(user_id, file_id, filename):
        try:
            file_id_encrypt = int(round(time.time() * 1000))
            user_path = '../storage/users/%s' % user_id

            key = Fernet.generate_key()
            key_file_path = '/keys/%s.key' % filename
            key_file = open(user_path + key_file_path, 'wb')
            key_file.write(key)
            key_file.close()

            db_file = DBfiles.get_user_file(file_id, user_id)
            unencrypted_file_path = db_file[0]['path']
            with open(user_path + unencrypted_file_path, 'rb') as f:
                data_file = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data_file)
            encrypted_filename = filename + '.encrypted'
            encrypted_file_path = '/files/encrypted/%s' % encrypted_filename
            with open(user_path + encrypted_file_path, 'wb') as f:
                f.write(encrypted)

            is_encrypted = 1
            DBfiles.insert_user_file(file_id_encrypt, user_id, encrypted_filename, encrypted_file_path, is_encrypted)
            DBfiles.insert_file_key(user_id, file_id_encrypt, key_file_path)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while encrypting the file'
        else:
            return 'Successfully encrypted the file'

    @staticmethod
    def decryption(user_id, file_id, filename):
        try:
            db_file_key = DBfiles.get_file_key(file_id, user_id)
            file_id_decrypt = int(round(time.time() * 1000))
            user_path = '../storage/users/%s' % user_id

            key_file_path = db_file_key[0]['key_path']
            with open(user_path + key_file_path, 'rb') as f:
                key = f.read()

            db_file = DBfiles.get_user_file(file_id, user_id)

            encrypted_file_path = db_file[0]['path']
            with open(user_path + encrypted_file_path, 'rb') as f:
                file = f.read()

            fernet = Fernet(key)
            decrypted = fernet.decrypt(file)

            decrypted_file_path = '/files/unencrypted/%s' % filename
            with open(user_path + decrypted_file_path, 'wb') as f:
                f.write(decrypted)

            is_encrypted = 0
            DBfiles.insert_user_file(file_id_decrypt, user_id, filename, decrypted_file_path, is_encrypted)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while decrypting the file'
        else:
            return 'Successfully decrypted the file'
