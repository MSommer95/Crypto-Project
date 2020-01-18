import cherrypy

from server.python.crypto_handling.hash_handler import HashHandler
from server.python.server_handling.input_validator import InputValidator


class AuthHandler:

    @staticmethod
    def check_for_auth(user_id):
        if InputValidator.check_session_value('2fa_status'):
            return InputValidator.check_session_value('2fa_verified')
        else:
            return user_id

    @staticmethod
    def check_auth_token(auth_token):
        return auth_token == InputValidator.check_session_value('auth_token')

    @staticmethod
    def check_auth_token_db(user_id):
        return HashHandler.check_auth_token(user_id, cherrypy.session.get('auth_token'),
                                            cherrypy.session.id)
