from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os


class User:

    def __init__(self, firstname, lastname, username, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email

    def create_user_db(self, password):

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        salt = os.urandom(64)

        digest.update(bytes(password, 'utf-8'))
        digest.update(salt)
        hashed_password = digest.finalize()

        print(self.firstname + ' ' + self.lastname + ' ' + hashed_password)
