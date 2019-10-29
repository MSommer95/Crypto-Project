from cryptography.fernet import Fernet


class FileEncryptor:

    @staticmethod
    def file_encryption(user_id, file):
        key = Fernet.generate_key()

        key_file = open('../storage/users/%s/keys/%s.key' % (user_id, file.filename), 'wb')
        key_file.write(key)
        key_file.close()

        with open('../storage/users/%s/files/%s' % (user_id, file.filename), 'rb') as f:
            data_file = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data_file)

        with open('../storage/users/%s/files/encrypted/%s.encrypted' % (user_id, file.filename), 'wb') as f:
            f.write(encrypted)

    @staticmethod
    def file_decryption(user_id, filename):
        with open('../storage/users/%s/keys/%s.key' % (user_id, filename), 'rb') as f:
            key = f.read()

        with open('../storage/users/%s/files/%s.encrypted' % (user_id, filename), 'rb') as f:
            file = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(file)

        with open('../storage/users/%s/files/%s' % (user_id, filename), 'wb') as f:
            f.write(decrypted)
