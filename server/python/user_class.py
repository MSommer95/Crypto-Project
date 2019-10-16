import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class User:

    def __init__(self, email):
        self.email = email

    def create_user_db(self, password):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        salt = os.urandom(64)

        digest.update(bytes(password, 'utf-8'))
        digest.update(salt)
        hashed_password = digest.finalize()

        print(hashed_password)
