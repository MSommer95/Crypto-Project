import time

from cryptography.fernet import Fernet

from server.python.db_handling.db_files import DBfiles


class FileEncryptor:

    # Funktion zum Verschlüsseln einer Datei
    @staticmethod
    def encryption(user_id, file_id, filename):
        try:
            file_id_encrypt = int(round(time.time() * 1000))
            user_path = f'../storage/users/{user_id}'

            key = Fernet.generate_key()
            key_file_path = f'/keys/{filename}.key'
            key_file = open(f'{user_path}{key_file_path}', 'wb')
            key_file.write(key)
            key_file.close()

            db_file = DBfiles.get_file(file_id, user_id)
            unencrypted_file_path = db_file[0]['path']
            with open(f'{user_path}{unencrypted_file_path}', 'rb') as f:
                data_file = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data_file)
            encrypted_filename = f'{filename}.encrypted'
            encrypted_file_path = f'/files/encrypted/{encrypted_filename}'
            with open(user_path + encrypted_file_path, 'wb') as f:
                f.write(encrypted)
            file_description = 'My encrypted file'
            is_encrypted = 1
            DBfiles.insert(file_id_encrypt, user_id, encrypted_filename, file_description, encrypted_file_path,
                           is_encrypted)
            DBfiles.insert_file_key(user_id, file_id_encrypt, key_file_path)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while encrypting the file'
        else:
            return 'Successfully encrypted the file'

    # Funktion zum Entschlüsseln einer Datei
    @staticmethod
    def decryption(user_id, file_id, filename):
        try:
            db_file_key = DBfiles.get_file_key(file_id, user_id)
            file_id_decrypt = int(round(time.time() * 1000))
            user_path = f'../storage/users/{user_id}'

            key_file_path = db_file_key[0]['key_path']
            with open(f'{user_path}{key_file_path}', 'rb') as f:
                key = f.read()

            db_file = DBfiles.get_file(file_id, user_id)

            encrypted_file_path = db_file[0]['path']
            with open(f'{user_path}{encrypted_file_path}', 'rb') as f:
                file = f.read()

            fernet = Fernet(key)
            decrypted = fernet.decrypt(file)

            decrypted_file_path = f'/files/unencrypted/{filename}'
            with open(f'{user_path}{decrypted_file_path}', 'wb') as f:
                f.write(decrypted)
            file_description = 'My decrypted file'
            is_encrypted = 0
            DBfiles.insert(file_id_decrypt, user_id, filename, file_description, decrypted_file_path, is_encrypted)
        except (RuntimeError, TypeError, NameError):
            return 'Something went wrong while decrypting the file'
        else:
            return 'Successfully decrypted the file'
