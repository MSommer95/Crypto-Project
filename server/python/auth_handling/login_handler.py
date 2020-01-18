import cherrypy

from server.python.comm_handling.email_sender import EmailSender
from server.python.crypto_handling.hash_handler import HashHandler
from server.python.crypto_handling.otp_handler import OtpHandler
from server.python.db_handling.db_otp import DBotp
from server.python.db_handling.db_tokens import DBtokens
from server.python.db_handling.db_users import DBusers
from server.python.server_handling.dir_handler import DirHandler
from server.python.server_handling.login_log_handler import LLogHandler
from server.python.server_handling.response_handler import ResponseHandler


class LoginHandler:

    @staticmethod
    def login_mail(user_id, email):
        cherrypy.session['2fa_status'] = 1
        cherrypy.session['otp_option'] = 1
        otp = OtpHandler.create_otp(user_id)
        DBotp.insert(user_id, otp)
        OtpHandler.send_otp_mail(email, otp)

    @staticmethod
    def login_app(user_id):
        cherrypy.session['2fa_status'] = 1
        cherrypy.session['otp_option'] = 2
        otp = OtpHandler.create_otp(user_id)
        DBotp.insert(user_id, otp)
        OtpHandler.send_otp_app(user_id, otp)

    @staticmethod
    def finalize_login(user_id, user_settings, auth_token, email):
        if user_settings['2FA-Mail'] == 1:
            LoginHandler.login_mail(user_id, email)
            response = {'token': auth_token, 'message': 'Please send us your OTP'}
            return response
        elif user_settings['2FA-App'] == 1:
            LoginHandler.login_app(user_id)
            response = {'token': auth_token, 'message': 'Please send us your OTP'}
            return response
        else:
            LoginHandler.regenerate_session(user_id)
            cherrypy.session['2fa_status'] = 0
            response = {'token': auth_token, 'message': 'Send me to index'}
            return response

    @staticmethod
    def prepare_login(user, user_id, email):
        if len(user) > 0:
            DirHandler.check_user_dirs(user_id)
            auth_token = HashHandler.create_auth_token(user_id, cherrypy.request.headers, cherrypy.session.id)
            user_settings = DBusers.get_user_settings(user_id)
            cherrypy.session['user_id'] = user['id']
            cherrypy.session['user_mail'] = user['email']
            cherrypy.session['2fa_verified'] = 0
            cherrypy.session['auth_token'] = auth_token
            return LoginHandler.finalize_login(user_id, user_settings, auth_token, email)
        else:
            return LoginHandler.fail_login(user_id, email)

    @staticmethod
    def send_reset_token(user_id, email):
        DBtokens.delete(user_id, 2)
        token = HashHandler.create_reset_token(user_id, 2)
        subject = 'Password Reset Token'
        message = f'Here is your reset token: {token}'
        EmailSender.send_mail(message, subject, email)
        return 'Token send to Email-address'

    @staticmethod
    def regenerate_session(user_id):
        cherrypy.session.regenerate()
        auth_token = HashHandler.create_auth_token(user_id, cherrypy.request.headers, cherrypy.session.id)
        cherrypy.session['auth_token'] = auth_token

    @staticmethod
    def verify_login(user_id):
        cherrypy.session['2fa_verified'] = 1
        DirHandler.check_user_dirs(user_id)
        LoginHandler.regenerate_session(user_id)

    @staticmethod
    def fail_login(user_id, email):
        user_logs = LLogHandler.check_login_logs(user_id)
        if LLogHandler.count_tries(user_id, user_logs, email):
            cherrypy.response.status = 403
            return ResponseHandler.unauthorized_response('Wrong Data. Please try again.')
        else:
            return ResponseHandler.too_many_requests_response('Too many tries')
