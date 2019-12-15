import binascii
import hashlib
import os
import secrets
import string
import time

from server.python.auth_handling.otp_handler import OtpHandler
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
        token = OtpHandler.create_random_string(alphabet, 16)
        hashed_token = HashHandler.hash_password(token)
        tokens = DBtokens.all()
        if hashed_token in tokens:
            HashHandler.create_token(user_id, reset_case)
            return
        else:
            DBtokens.insert(user_id, hashed_token, reset_case)
            return token

    @staticmethod
    def create_auth_token(user_id, headers, session_id):
        bit_number = secrets.randbits(64)
        user_agent = headers['User-Agent']
        host = headers['Host']
        millis = int(round(time.time() * 1000))
        pre_hashed = str(bit_number) + user_agent + host + str(millis)
        salt = HashHandler.get_server_salt()
        token = hashlib.sha256(salt.encode() + pre_hashed.encode()).hexdigest()
        hashed_token = HashHandler.hash_password(token)
        tokens = DBtokens.all_auth_token()
        hashed_session_id = HashHandler.hash_password(session_id)
        if hashed_token in tokens:
            HashHandler.create_auth_token(user_id, headers, session_id)
            return
        else:
            DBtokens.insert_auth_token(user_id, hashed_token, hashed_session_id)
            return token

    @staticmethod
    def check_token(user_id, token, reset_case):
        db_token = DBtokens.get(user_id, reset_case)[0]['token']
        return HashHandler.verify_password(db_token, token)

    @staticmethod
    def check_auth_token(user_id, token, session_id):
        db_result = DBtokens.get_auth_token(user_id)[0]
        db_session_id = db_result['session_id']
        return HashHandler.verify_password(db_result['token'], token) and HashHandler.verify_password(db_session_id,
                                                                                                      session_id)

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

    @staticmethod
    def md5(message):
        md5_hash = hashlib.md5(message.encode())
        return md5_hash.hexdigest()

    @staticmethod
    def sha1(message):
        sha1_hash = hashlib.sha1(message.encode())
        return sha1_hash.hexdigest()

    @staticmethod
    def blake2b(message):
        blake2b_hash = hashlib.blake2b(message.encode())
        return blake2b_hash.hexdigest()

    @staticmethod
    def blake2s(message):
        blake2s_hash = hashlib.blake2s(message.encode())
        return blake2s_hash.hexdigest()

    @staticmethod
    def sha256(message):
        sha256_hash = hashlib.sha256(message.encode())
        return sha256_hash.hexdigest()

    @staticmethod
    def sha512(message):
        sha512_hash = hashlib.sha512(message.encode())
        return sha512_hash.hexdigest()

    @staticmethod
    def sha3_256(message):
        sha3_256_hash = hashlib.sha3_256(message.encode())
        return sha3_256_hash.hexdigest()

    @staticmethod
    def sha3_512(message):
        sha3_512_hash = hashlib.sha3_512(message.encode())
        return sha3_512_hash.hexdigest()

    @staticmethod
    def shake_128(message):
        shake_128_hash = hashlib.shake_128(message.encode())
        return shake_128_hash.hexdigest(128)

    @staticmethod
    def shake_256(message):
        shake_256_hash = hashlib.shake_256(message.encode())
        return shake_256_hash.hexdigest(256)

    @staticmethod
    def choose_hash_function(function, message):
        if function == 'md5':
            return HashHandler.md5(message)
        elif function == 'sha1':
            return HashHandler.sha1(message)
        elif function == 'blake2(s)':
            return HashHandler.blake2s(message)
        elif function == 'blake2(b)':
            return HashHandler.blake2b(message)
        elif function == 'sha256':
            return HashHandler.sha256(message)
        elif function == 'sha512':
            return HashHandler.sha512(message)
        elif function == 'sha3(256)':
            return HashHandler.sha3_256(message)
        elif function == 'sha3(512)':
            return HashHandler.sha3_512(message)
        elif function == 'shake(128)':
            return HashHandler.shake_128(message)
        elif function == 'shake(256)':
            return HashHandler.shake_256(message)
