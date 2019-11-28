import binascii
import hashlib
import os
import random
import string
from server.python.db_handling.db_tokens import DBtokens


class HashHandler:

    @staticmethod
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                       salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        return (salt + pwd_hash).decode('ascii')

    @staticmethod
    def create_token(user_id):
        token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
        tokens = DBtokens.all()

        if token in tokens:
            HashHandler.create_token(user_id)
            return
        else:
            DBtokens.insert(user_id, token)
            return token

    @staticmethod
    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwd_hash = hashlib.pbkdf2_hmac('sha512',
                                       provided_password.encode('utf-8'),
                                       salt.encode('ascii'),
                                       100000)
        pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
        return pwd_hash == stored_password
