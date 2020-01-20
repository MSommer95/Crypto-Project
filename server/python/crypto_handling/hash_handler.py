import binascii
import hashlib
import os
import secrets
import string
import time

from server.python.crypto_handling.otp_handler import OtpHandler
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
    def hash_string(provided_string, algorithm, rounds):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        hashed_string = hashlib.pbkdf2_hmac(algorithm, provided_string.encode('utf-8'),
                                            salt, rounds)
        hashed_string = binascii.hexlify(hashed_string)
        return (salt + hashed_string).decode('ascii')

    @staticmethod
    def verify_hash(stored_hash, provided_string, algorithm, rounds):
        salt = stored_hash[:64]
        stored_hash = stored_hash[64:]
        provided_hash = hashlib.pbkdf2_hmac(algorithm,
                                            provided_string.encode('utf-8'),
                                            salt.encode('ascii'),
                                            rounds)
        provided_hash = binascii.hexlify(provided_hash).decode('ascii')
        return provided_hash == stored_hash

    @staticmethod
    def create_reset_token(user_id, reset_case):
        alphabet = f'{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}'
        token = OtpHandler.create_random_string(alphabet, 16)
        hashed_token = HashHandler.hash_string(token, 'sha512', 10000)
        tokens = DBtokens.all()
        if hashed_token in tokens:
            HashHandler.create_reset_token(user_id, reset_case)
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
        hashed_token = HashHandler.hash_string(token, 'sha256', 1)
        tokens = DBtokens.all_auth_token()
        hashed_session_id = HashHandler.hash_string(session_id, 'sha256', 1)
        if hashed_token in tokens:
            HashHandler.create_auth_token(user_id, headers, session_id)
            return
        else:
            DBtokens.insert_auth_token(user_id, hashed_token, hashed_session_id)
            return token

    @staticmethod
    def check_token(user_id, token, reset_case):
        db_token = DBtokens.get(user_id, reset_case)[0]['token']
        return HashHandler.verify_hash(db_token, token, 'sha512', 10000)

    @staticmethod
    def check_auth_token(user_id, token, session_id):
        db_result = DBtokens.get_auth_token(user_id)[0]
        db_session_id = db_result['session_id']
        return HashHandler.verify_hash(db_result['token'], token, 'sha256', 1) and HashHandler.verify_hash(
            db_session_id,
            session_id, 'sha256', 1)

    @staticmethod
    def choose_hash_function(function, message):
        if function == 'md5':
            return hashlib.md5(message.encode()).hexdigest()
        elif function == 'sha1':
            return hashlib.sha1(message.encode()).hexdigest()
        elif function == 'blake2(s)':
            return hashlib.blake2b(message.encode()).hexdigest()
        elif function == 'blake2(b)':
            return hashlib.blake2s(message.encode()).hexdigest()
        elif function == 'sha256':
            return hashlib.sha256(message.encode()).hexdigest()
        elif function == 'sha512':
            return hashlib.sha512(message.encode()).hexdigest()
        elif function == 'sha3(256)':
            return hashlib.sha3_256(message.encode()).hexdigest()
        elif function == 'sha3(512)':
            return hashlib.sha3_512(message.encode()).hexdigest()
        elif function == 'shake(128)':
            return hashlib.shake_128(message.encode()).hexdigest(128)
        elif function == 'shake(256)':
            return hashlib.shake_256(message.encode()).hexdigest(256)
