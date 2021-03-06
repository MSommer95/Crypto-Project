import base64
import os

import cherrypy
from cherrypy.lib.static import serve_file

from server.python.auth_handling.auth_handler import AuthHandler
from server.python.auth_handling.login_handler import LoginHandler
from server.python.auth_handling.second_factor_handling import SecondFactorHandler
from server.python.comm_handling.qr_handler import QRHandler
from server.python.crypto_handling.caesar_cipher import CaesarCipher
from server.python.crypto_handling.cipher_helper import CipherHelper
from server.python.crypto_handling.hash_handler import HashHandler
from server.python.crypto_handling.otp_handler import OtpHandler
from server.python.crypto_handling.vigenere_cipher import VigenereCipher
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_files import DBfiles
from server.python.db_handling.db_otp import DBotp
from server.python.db_handling.db_tokens import DBtokens
from server.python.db_handling.db_users import DBusers
from server.python.file_handling.file_encryptor import FileEncryptor
from server.python.file_handling.file_handler import FileHandler
from server.python.server_handling.dir_handler import DirHandler
from server.python.server_handling.input_validator import InputValidator
from server.python.server_handling.response_handler import ResponseHandler
from server.python.user_handling.settings_handler import SettingsHandler


class CryptoServer(object):

    @cherrypy.expose()
    def index(self):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token_db(user_id):
            return ResponseHandler.prepare_index(user_id)
        else:
            ResponseHandler.unauthorized_response('You are unauthorized')
            raise cherrypy.HTTPRedirect('/sign')

    @cherrypy.expose()
    def sign(self, **params):
        if len(params) > 0:
            ResponseHandler.unauthorized_response(params['message'])
            return open('../public/dist/sign.html')
        else:
            return open('../public/dist/sign.html')

    @cherrypy.expose()
    def create_account(self, email, password):
        email_check = DBusers.get_user_id(email)
        if InputValidator.email_validator(email) and len(password) > 0 and len(email_check) == 0:
            user_id = DBusers.insert_user(email, password)
            DirHandler.check_user_dirs(str(user_id))
            LoginHandler.prepare_login(DBusers.check_user(email, password), user_id, email)
            raise cherrypy.HTTPRedirect('/index')
        else:
            raise cherrypy.HTTPRedirect('/sign?message=Invalid Email')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def login_account(self, email, password):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]
            if len(user_id) > 0:
                user = DBusers.check_user(email, password)
                return LoginHandler.prepare_login(user, str(user_id['id']), email)
            else:
                return ResponseHandler.forbidden_response('Not authorized')
        else:
            return ResponseHandler.bad_request_response('Not a valid email address')

    @cherrypy.expose()
    def login_account_app(self, device_id):
        device = DBdevices.get_by_device_id(device_id)
        if len(device) > 0:
            if device[0]['device_is_active']:
                return 'Login successful'
        return 'Device unauthorized, please register and activate this device'

    @cherrypy.expose()
    def logout_account(self):
        cherrypy.lib.sessions.expire()
        return 'You are logged out'

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def verify_otp(self, otp, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return LoginHandler.prepare_otp_login(user_id, otp)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    def verify_otp_app(self, otp, user_id):
        check_value = DBotp.check_current(user_id, otp)
        if check_value:
            DBotp.update_verification(user_id)
            return 'Verification valid'
        else:
            return 'Verification invalid'

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def check_otp_verified(self):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token_db(user_id):
            check_value = DBotp.check_verification(user_id)
            if check_value:
                LoginHandler.verify_login(user_id)
            return ResponseHandler.success_response(str(check_value))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    def file_upload(self, file, file_description, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if not InputValidator.file_validator(file):
            ResponseHandler.bad_request_response('You didnt submit a valid file')
            return cherrypy.HTTPRedirect('/')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            FileHandler.write_file(user_id, file, file_description)
            raise cherrypy.HTTPRedirect('/')
        else:
            ResponseHandler.unauthorized_response('You are unauthorized')
            raise cherrypy.HTTPRedirect('/sign')

    @cherrypy.expose()
    def file_download(self, file_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            user_path = f'../storage/users/{user_id}'
            absolute_file_path = os.path.abspath(f'{user_path}{DBfiles.get_file_path(user_id, file_id)}')
            file_name = DBfiles.get_file_name(file_id, user_id)
            return serve_file(absolute_file_path, disposition="attachment", name=file_name)
        else:
            ResponseHandler.unauthorized_response('You are unauthorized')
            raise cherrypy.HTTPRedirect('/sign')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def file_encrypt(self, file_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return ResponseHandler.success_response(FileEncryptor.encrypt(user_id, file_id))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def file_decrypt(self, file_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return ResponseHandler.success_response(FileEncryptor.decrypt(user_id, file_id))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def file_update(self, file_id, file_description, file_name, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            message = FileHandler.change_file_name(user_id, file_id, file_name, file_description)
            return ResponseHandler.success_response(message)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def file_delete(self, file_id, is_encrypted, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            message = FileHandler.delete_file(user_id, file_id, DBfiles.get_file_path(user_id, file_id), is_encrypted)
            return ResponseHandler.success_response(message)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_files(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            files = DBfiles.get_files(user_id)
            return files
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_used_otps(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return OtpHandler.prepare_used_otps(user_id)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_devices(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            devices = DBdevices.get_by_user_id(user_id)
            return devices
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def insert_user_device(self, device_id, device_name, user_id):
        if not user_id:
            user_id = InputValidator.check_session_value('user_id')
            if AuthHandler.check_for_auth(user_id):
                user_id = str(user_id)
            else:
                return ResponseHandler.unauthorized_response('You are unauthorized')
        device = DBdevices.get_by_device_id(device_id)
        if len(device) > 0:
            if device[0]['device_is_active']:
                return 'Device already active'
            else:
                return 'Device already registered'
        db_connection_state = DBdevices.insert(user_id, device_id, device_name)
        if db_connection_state == 'success':
            return 'Successfully inserted device'
        elif db_connection_state == 'failed':
            return 'Failed to insert device'

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def delete_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            DBdevices.delete(device_id, user_id)
            deleted_message = f'Device was deleted. \n {SecondFactorHandler.check_for_active_device(user_id)}'
            return ResponseHandler.success_response(deleted_message)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def activate_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            DBdevices.deactivate_all(user_id)
            return ResponseHandler.success_response(SecondFactorHandler.activate_device(user_id, device_id))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def deactivate_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            deactivate_message = SecondFactorHandler.deactivate_device(user_id, device_id)
            deactivate_addition = SecondFactorHandler.check_for_active_device(user_id)
            return ResponseHandler.success_response(f'{deactivate_message} {deactivate_addition}')
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_settings(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return DBusers.get_user_settings(user_id)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def update_account_info(self, email, password, old_password, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(
                auth_token) and InputValidator.email_validator(email):
            user_id = str(user_id)
            user_mail = InputValidator.check_session_value('user_mail')
            message = SettingsHandler.update_account_info(user_id, user_mail, email, password, old_password)
            return ResponseHandler.success_response(message)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def update_settings_sec_fa(self, sec_fa, sec_fa_email, sec_fa_app, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            message = SettingsHandler.check_second_factor_options(sec_fa, sec_fa_email, sec_fa_app, user_id)
            return ResponseHandler.success_response(message)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def reset_settings_sec_fa(self, token):
        user_id = InputValidator.check_session_value('user_id')
        if user_id:
            if HashHandler.check_token(user_id, token, 1):
                SecondFactorHandler.deactivate_both_second_factor_options(user_id)
                return ResponseHandler.success_response('Successfully disabled second factor. Please login again.')
            else:
                return ResponseHandler.forbidden_response('Wrong token')
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def request_password_reset(self, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                return ResponseHandler.success_response(LoginHandler.send_reset_token(user_id, email))
            else:
                return ResponseHandler.unauthorized_response('You are unauthorized')
        else:
            return ResponseHandler.bad_request_response('Not a valid email address')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def password_reset(self, token, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                if HashHandler.check_token(user_id, token, 2):
                    return ResponseHandler.success_response('Correct token')
                else:
                    return ResponseHandler.forbidden_response('Wrong token')
            else:
                return ResponseHandler.unauthorized_response('You are unauthorized')
        else:
            return ResponseHandler.bad_request_response('Not a valid email address')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def new_password(self, password, token, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                if HashHandler.check_token(user_id, token, 2):
                    if len(DBusers.check_user(email, password)) == 0:
                        DBtokens.delete(user_id, 2)
                        return ResponseHandler.success_response(DBusers.update_password(user_id, password))
                    else:
                        return ResponseHandler.forbidden_response('Do not use your old password!')
                else:
                    return ResponseHandler.forbidden_response('Wrong token')
            else:
                return ResponseHandler.unauthorized_response('You are unauthorized')
        else:
            return ResponseHandler.bad_request_response('Not a valid email address')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def authenticate_app(self, email, password, device_id, device_name):
        print(device_id)
        user = DBusers.check_user(email, password)
        user_count = len(user)
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        if user_count > 0:
            cherrypy.session['user_id'] = user['id']
            cherrypy.session['2fa_status'] = 0
            user_id = str(user['id'])
            user_settings = DBusers.get_user_settings(user_id)
            if user_settings['2FA-App'] and user_settings['2FA-App'] == 1:
                devices = DBdevices.get_by_user_id(user_id)
                print(str(devices))
                if len(devices) > 0 and any(x['device_id'] == device_id for x in devices):
                    device = {}

                    for x in devices:
                        if x['device_id'] == device_id:
                            device = x

                    if device['device_is_active'] and device['device_is_active'] == 1:
                        cherrypy.session['2fa_status'] = 1
                        response = {'status': 200, 'message': 'Success'}
                        print('response', str(response))
                        return response
                    else:
                        response = {'status': 403, 'message': 'Device must be activated in web-interface'}
                        return response
                else:
                    DBdevices.insert(user_id, device_id, device_name)
                    response = {'status': 403, 'message': 'Device added, but must be activated in web-interface'}
                    return response
            else:
                response = {'status': 403, 'message': 'App auth inactive'}
                return response
        else:
            response = {'status': 403, 'message': 'No such user found or password wrong'}
            return response

    @cherrypy.expose()
    def request_otp_app(self, device_id):
        device = DBdevices.get_by_device_id(device_id)
        if len(device) == 0:
            return
        user_id = str(device[0]['user_id'])
        user_settings = DBusers.get_user_settings(user_id)
        if user_settings['2FA-App'] == 1:
            otp = OtpHandler.create_otp(user_id)
            DBotp.insert(user_id, otp)
            return otp

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def request_new_otp(self):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token_db(user_id):
            user_id = str(user_id)
            user_mail = InputValidator.check_session_value('user_mail')
            otp_option = InputValidator.check_session_value('otp_option')
            return ResponseHandler.success_response(OtpHandler.prepare_otp_send(user_id, otp_option, user_mail))
        else:
            ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    def request_qr(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            otp = OtpHandler.create_otp(user_id)
            DBotp.insert(user_id, otp)
            img_string = QRHandler.create_qr_image(user_id, otp)
            cherrypy.response.headers['Content-Type'] = "image/png"
            return base64.b64encode(img_string)
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    def request_top_password(self):
        return open('../storage/other/top500passwords')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def hash_message(self, hash_function, message, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            return ResponseHandler.success_response(HashHandler.choose_hash_function(hash_function, message))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def caesar_cipher(self, message, shift, option, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if not InputValidator.int_validator(int(shift)):
            return ResponseHandler.bad_request_response('Your Shift value has to be an int')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            return ResponseHandler.success_response(CaesarCipher(int(shift)).cipher(message, option))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def caesar_cipher_crack(self, message, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            return ResponseHandler.success_response(CaesarCipher(0).crack_cipher(message))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def vigenere_cipher(self, message, key, option, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            clean_message = CipherHelper.remove_special_chars(message)
            return ResponseHandler.success_response(VigenereCipher().cipher(clean_message, key, option))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def vigenere_cipher_crack(self, message, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            clean_message = CipherHelper.remove_special_chars(message)
            return ResponseHandler.success_response(VigenereCipher().crack_cipher(clean_message))
        else:
            return ResponseHandler.unauthorized_response('You are unauthorized')


if __name__ == '__main__':
    os.chdir('../')


    def force_tls():
        if cherrypy.request.scheme == "http":
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("http:", "https:"),
                                        status=301)


    cherrypy.tools.force_tls = cherrypy.Tool("before_handler", force_tls)


    def load_http_server():
        server = cherrypy._cpserver.Server()
        server.socket_port = 80
        server.subscribe()


    # LogHandler.get_access_log('access')
    @cherrypy.tools.register('before_finalize', priority=60)
    def secure_headers():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['X-Content-Type-Options'] = 'nosniff'
        headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        headers['Pragma'] = 'no-cache'
        # headers['Content-Security-Policy'] = "default-src 'self';"


    conf = os.path.join(os.path.dirname(__file__) + '/conf/', 'server_conf')
    DirHandler.check_server_dirs()
    HashHandler.new_server_salt()
    load_http_server()
    cherrypy.tree.mount(CryptoServer(), '/', config=conf)
    cherrypy.config.update(conf)
    cherrypy.config.update(
        {'error_page.404': os.path.join(os.path.dirname(__file__) + '/error_templates/', '404.html')})
    cherrypy.config.update(
        {'error_page.500': os.path.join(os.path.dirname(__file__) + '/error_templates/', '500.html')})
    cherrypy.engine.start()
