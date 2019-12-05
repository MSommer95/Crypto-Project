import binascii
import hashlib
import os
import secrets
import string
import time

from server.python.db_handling.db_tokens import DBtokens


class HashHandler:

    @staticmethod
    def new_server_salt():
        salt = str(secrets.randbits(64))
        with open('../storage/salt/salt.txt', 'w') as f:
            f.write(salt)

    @staticmethod
    def get_server_salt():
        with open('../storage/salt/salt.txt', 'r') as f:
            salt = f.read()
        return salt

    @staticmethod
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                       salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        return (salt + pwd_hash).decode('ascii')

    @staticmethod
    def create_token(user_id, reset_case):
        alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
        token = ''.join(secrets.choice(alphabet) for i in range(16))
        hashed_token = HashHandler.hash_password(token)
        tokens = DBtokens.all()
        if hashed_token in tokens:
            HashHandler.create_token(user_id, reset_case)
            return
        else:
            DBtokens.insert(user_id, hashed_token, reset_case)
            return token

    @staticmethod
    def create_auth_token(user_id, headers):
        bit_number = secrets.randbits(64)
        user_agent = headers['User-Agent']
        host = headers['Host']
        millis = int(round(time.time() * 1000))
        pre_hashed = str(bit_number) + user_agent + host + str(millis)
        salt = HashHandler.get_server_salt()
        token = hashlib.sha256(salt.encode() + pre_hashed.encode()).hexdigest()
        hashed_token = HashHandler.hash_password(token)
        tokens = DBtokens.all_auth_token()
        if hashed_token in tokens:
            HashHandler.create_auth_token(user_id, headers)
            return
        else:
            DBtokens.insert_auth_token(user_id, token)
            return token

    @staticmethod
    def check_token(user_id, token, reset_case):
        db_token = DBtokens.get(user_id, reset_case)[0]['token']
        return HashHandler.verify_password(db_token, token)

    @staticmethod
    def check_auth_token(user_id, token):
        db_token = DBtokens.get_auth_token(user_id)[0]['token']
        return db_token == token

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
