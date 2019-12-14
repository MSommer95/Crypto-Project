import base64
import os

import cherrypy
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader

from server.python.auth_handling.hash_handler import HashHandler
from server.python.auth_handling.login_handler import LoginHandler
from server.python.auth_handling.otp_handler import OtpHandler
from server.python.auth_handling.second_factor_handling import SecondFactorHandler
from server.python.comm_handling.qr_handler import QRHandler
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_files import DBfiles
from server.python.db_handling.db_otp import DBotp
from server.python.db_handling.db_tokens import DBtokens
from server.python.db_handling.db_users import DBusers
from server.python.file_handling.file_encryptor import FileEncryptor
from server.python.file_handling.file_handler import FileHandler
from server.python.server_handling.auth_handler import AuthHandler
from server.python.server_handling.dir_handler import DirHandler
from server.python.server_handling.input_validator import InputValidator
from server.python.server_handling.login_log_handler import LLogHandler
from server.python.server_handling.response_handler import ResponseHandler
from server.python.user_handling.settings_handler import SettingsHandler

ENV = Environment(loader=FileSystemLoader('/server/'))


class CryptoServer(object):

    # Index Call Function: Bearbeitet die Index Request der Website. Solange keine user_id gesetzt wurde,
    # wird der User auf die Login Seite redirected Überprüft die Session darauf, ob die 2fa aktiviert ist und ob der
    # 2te Faktor schon bestätigt wurde
    @cherrypy.expose()
    def index(self):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token_db(user_id):
            return LLogHandler.prepare_index(user_id)
        else:
            ResponseHandler.unauthorized_response()
            return open('../public/dist/sign.html')

    # Sign redirect
    @cherrypy.expose()
    def sign(self):
        return open('../public/dist/sign.html')

    # create Funktion nimmt eine Emailadresse und Passwort entgegen und erstellt einen account in der DB + die
    # zugehörige Ordner Struktur
    @cherrypy.expose()
    def create_account(self, email, password):
        if InputValidator.email_validator(email) and len(password) > 0:
            DirHandler.create_user_dirs(str(DBusers.insert_user(email, password)))
            return 'Account created'
        else:
            return ResponseHandler.bad_request_response()

    # login Funktion nimmt Emailadresse und Passwort entgegen und überprüft, ob ein user existiert und ob das
    # passwort stimmt. Innere if Abfrage checked, welche settings der User aktiviert hat und initialisiert die
    # jeweiligen Session Variablen
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def login_account(self, email, password):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)
            if len(user_id) > 0:
                user_id = user_id[0]['id']
                user_logs = LLogHandler.check_login_logs(user_id)
                if LLogHandler.count_tries(user_id, user_logs, email):
                    user = DBusers.check_user(email, password)
                    return LoginHandler.prepare_login(user, user_id, email)
                else:
                    return ResponseHandler.too_many_requests_response()
            else:
                return ResponseHandler.forbidden_response()
        else:
            return ResponseHandler.bad_request_response()

    # Funktion zum automatischen Login innerhalb der App, benötigt die id des vom Nutzer aktivierten Gerätes zum
    # erfolgreichen Login
    @cherrypy.expose()
    def login_account_app(self, device_id):
        device = DBdevices.get_by_device_id(device_id)
        if len(device) > 0:
            if device[0]['device_is_active']:
                return 'Login successful'
        return 'Device unauthorized, please register and activate this device'

    # Funktion zum Ausloggen des Nutzers, beendet die derzeitige Session und entfernt damit verbundenene Session-Daten
    @cherrypy.expose()
    def logout_account(self):
        cherrypy.lib.sessions.expire()
        return 'You are logged out'

    # verify Funktion überprüft, ob der eingegebene otp gültig ist (Innerhalb des Zeitraums und richtiger Code)
    @cherrypy.expose()
    def verify_otp(self, otp, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            check_value = DBotp.check_current(user_id, otp)
            if check_value:
                LoginHandler.verify_login(user_id)
                return 'Verification valid'
            else:
                return ResponseHandler.forbidden_response()
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zur Überprüfung eines per App gesendeten One-Time-Passwords, gültige Passwörter sind unbenutzt und
    # nicht älter als eine Minute
    @cherrypy.expose()
    def verify_otp_app(self, otp, user_id):
        check_value = DBotp.check_current(user_id, otp)
        if check_value:
            DBotp.update_verification(user_id)
            return 'Verification valid'
        else:
            return 'Verification invalid'

    # Funktion zur Überprüfung der Gültigkeit eines One-Time-Passwords, gültige Passwörter sind unbenutzt und nicht
    # älter als eine Minute
    @cherrypy.expose()
    def check_otp_verified(self):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token_db(user_id):
            check_value = DBotp.check_verification(user_id)
            if check_value:
                LoginHandler.verify_login(user_id)
            return str(check_value)
        else:
            return ResponseHandler.unauthorized_response()

    # upload Funktion nimmt eine file als Parameter entgegen und schreib sie in den unencrypted Fileordner des Users
    # nach dem Speichern der Datei wird die Datei verschlüsselt in den encrypted Ordner gelegt
    @cherrypy.expose()
    def file_upload(self, file, file_description, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            FileHandler.write_file(user_id, file, file_description)
            return open('../public/dist/index.html')
        else:
            ResponseHandler.unauthorized_response()
            return open('../public/dist/sign.html')

    # Funktion zum Herunterladen einer bestehenden Datei des Nutzers auf dem Server
    @cherrypy.expose()
    def file_download(self, file_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            user_path = '../storage/users/%s' % user_id
            absolute_file_path = os.path.abspath(user_path + DBfiles.get_file_path(user_id, file_id))
            return serve_file(absolute_file_path, disposition="attachment")
        else:
            ResponseHandler.unauthorized_response()
            return open('../public/dist/sign.html')

    # encryption Funktion nimmt einen Filename entgegen und verschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_encrypt(self, file_id, file_name, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return FileEncryptor.encryption(user_id, file_id, file_name)
        else:
            return ResponseHandler.unauthorized_response()

    # decryption Funktion nimmt einen Filename entgegen und entschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_decrypt(self, file_id, file_name, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            file_name = file_name.strip('.encrypted')
            return FileEncryptor.decryption(user_id, file_id, file_name)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zur Änderung einer bestehenden hochgeladenen Datei des Nutzers
    @cherrypy.expose()
    def file_update(self, file_id, file_description, file_name, is_encrypted, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return FileHandler.change_file_name(user_id, file_id, file_name, DBfiles.get_file_path(user_id, file_id),
                                                is_encrypted, file_description)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Entfernen einer hochgeladenen Datei des Nutzers
    @cherrypy.expose()
    def file_delete(self, file_id, is_encrypted, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return FileHandler.delete_file(user_id, file_id, DBfiles.get_file_path(user_id, file_id), is_encrypted)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Auslesen aller hochgeladenen Dateien des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_files(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            files = DBfiles.get_files(user_id)
            return files
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Auslesen aller bereits genutzten OTP's des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_used_otps(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return OtpHandler.prepare_used_otps(user_id)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Auslesen aller registrierten Nutzer-Devices
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_devices(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            devices = DBdevices.get_by_user_id(user_id)
            return devices
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Hinzufügen eines neuen Nutzer-Devices, genutzt für Authentifikation per App als zweiten Faktor
    @cherrypy.expose()
    def insert_user_device(self, device_id, device_name, user_id):
        if not user_id:
            user_id = InputValidator.check_session_value('user_id')
            if AuthHandler.check_for_auth(user_id):
                user_id = str(user_id)
            else:
                return ResponseHandler.unauthorized_response()
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

    # Funktion zum Löschen eines Nutzer-Devices
    @cherrypy.expose()
    def delete_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            DBdevices.delete(device_id, user_id)
            deleted_message = 'Device was deleted. \n' + SecondFactorHandler.check_for_active_device(user_id)
            return deleted_message
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Aktivieren eines bereits existenten Devices für die 2-Faktor-Authentifikation, es kann nur jeweils
    # ein Device gleichzeitig aktiver zweiter Faktor sein
    @cherrypy.expose()
    def activate_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            DBdevices.deactivate_all(user_id)
            return SecondFactorHandler.activate_device(user_id, device_id)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Deaktivieren eines aktiven 2-Faktor-Devices des Nutzers
    @cherrypy.expose()
    def deactivate_user_device(self, device_id, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            deactived_message = SecondFactorHandler.deactivate_device(user_id, device_id)
            deactivae_addition = SecondFactorHandler.check_for_active_device(user_id)
            return '%s %s' % (deactived_message, deactivae_addition)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Auslesen der gewählten 2-Faktor-Eistellungen des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_settings(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return SettingsHandler.prepare_user_settings(user_id)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum Ändern des Passworts oder der Email eines Nutzers
    @cherrypy.expose()
    def update_account_info(self, email, password, old_password, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token) and InputValidator.email_validator(email):
            user_id = str(user_id)
            user_mail = InputValidator.check_session_value('user_mail')
            return SettingsHandler.update_account_info(user_id, user_mail, email, password, old_password)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum anpassen der 2-Faktor-Einstellungen des Nutzers, bei Aktivierung der 2-Faktor Authentifikation
    # wird ein einmaliges Token zum Zurücksetzen der Einlstellungen generiert und in der Datenbank gespeichert
    @cherrypy.expose()
    def update_settings_sec_fa(self, sec_fa, sec_fa_email, sec_fa_app, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            return SettingsHandler.check_second_factor_options(sec_fa, sec_fa_email, sec_fa_app, user_id)
        else:
            return ResponseHandler.unauthorized_response()

    # Funktion zum zurücksetzen der 2-Faktor Authentifizierung mittels Token, falls Nutzer Zugang zum
    # Authentifikationsmedium verliert
    @cherrypy.expose()
    def reset_settings_sec_fa(self, token):
        user_id = InputValidator.check_session_value('user_id')
        if user_id:
            if HashHandler.check_token(user_id, token, 1):
                SecondFactorHandler.deactivate_both_second_factor_options(user_id)
                return 'Successfully disabled second factor. Please login again.'
            else:
                return ResponseHandler.forbidden_response()
        else:
            return ResponseHandler.unauthorized_response()

    @cherrypy.expose()
    def request_password_reset(self, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                return LoginHandler.send_reset_token(user_id, email)
            else:
                return ResponseHandler.unauthorized_response()
        else:
            return ResponseHandler.bad_request_response()

    @cherrypy.expose()
    def password_reset(self, token, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                if HashHandler.check_token(user_id, token, 2):
                    return 'valid token'
                else:
                    return 'Wrong Token'
            else:
                return ResponseHandler.unauthorized_response()
        else:
            return ResponseHandler.bad_request_response()

    @cherrypy.expose()
    def new_password(self, password, token, email):
        if InputValidator.email_validator(email):
            user_id = DBusers.get_user_id(email)[0]['id']
            if user_id:
                if HashHandler.check_token(user_id, token, 2):
                    if len(DBusers.check_user(email, password)) == 0:
                        DBtokens.delete(user_id, 2)
                        return DBusers.update_password(user_id, password)
                    else:
                        return 'Do not use your old password!'
                else:
                    return ResponseHandler.unauthorized_response()
            else:
                return ResponseHandler.unauthorized_response()
        else:
            return ResponseHandler.bad_request_response()

    # Funktion zum Registrieren des Devices per App mittels Email und Passwort, falls App als 2-Faktor Authentifikator
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
                    cherrypy.session['2fa_status'] = 1
                    response = {'status': 200, 'message': 'Success'}
                    print('response', str(response))
                    return response
                else:
                    DBdevices.insert(user_id, device_id, device_name)
                    response = {'status': 200, 'message': 'Device added'}
                    return response
            else:
                response = {'status': 403, 'message': 'App auth inactive'}
                return response
        else:
            response = {'status': 403, 'message': 'No such user found or password wrong'}
            return response

    # Funktion zum Erstellen und Senden eines One-Time-Passwords, falls App als 2-Faktor Authentifikator genutzt wird
    @cherrypy.expose()
    def request_otp_app(self, device_id):
        device = DBdevices.get_by_device_id(device_id)
        if len(device) == 0:
            return
        user_id = str(device[0]['user_id'])
        user_settings = DBusers.get_user_settings(user_id)
        if user_settings['2FA-App'] and user_settings['2FA-App'] == 1:
            otp = OtpHandler.create_otp(user_id)
            DBotp.insert(user_id, otp)
            return otp

    # Function um einen neuen OTP zu requesten
    @cherrypy.expose()
    def request_new_otp(self):
        user_id = InputValidator.check_session_value('user_id')
        if user_id and AuthHandler.check_auth_token_db(user_id):
            user_id = str(user_id)
            user_mail = InputValidator.check_session_value('user_mail')
            otp_option = InputValidator.check_session_value('otp_option')
            return OtpHandler.prepare_otp_send(user_id, otp_option, user_mail)

    # Funktion zum erstellen eines QR-Code Bildes auf Basis der Daten user_id und otp im JSON Format, kann in der App
    # gescanned werden um Registrierung und Login zu vereinfachen
    @cherrypy.expose()
    def request_qr(self, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            user_id = str(user_id)
            otp = OtpHandler.create_otp(user_id)
            img_string = QRHandler.create_qr_image(user_id, otp)
            cherrypy.response.headers['Content-Type'] = "image/png"
            return base64.b64encode(img_string)
        else:
            return ResponseHandler.unauthorized_response()

    @cherrypy.expose()
    def request_top_password(self):
        return open('../storage/other/top500passwords')

    @cherrypy.expose()
    def hash_message(self, hash_function, message, auth_token):
        user_id = InputValidator.check_session_value('user_id')
        if AuthHandler.check_for_auth(user_id) and AuthHandler.check_auth_token(auth_token):
            return HashHandler.choose_hash_function(hash_function, message)
        else:
            return ResponseHandler.unauthorized_response()


if __name__ == '__main__':
    os.chdir('../')

    # LogHandler.get_access_log('access')
    @cherrypy.tools.register('before_finalize', priority=60)
    def secure_headers():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        # headers['Content-Security-Policy'] = "default-src 'self';"


    conf = {
        'global': {
            'server.socket_port': 8000,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': '../storage/ca/cert.pem',
            'server.ssl_private_key': '../storage/ca/privkey.pem'
        },
        '/': {
            'tools.secure_headers.on': True,
            'tools.sessions.on': True,
            'tools.sessions.timeout': 20,
            'tools.sessions.secure': True,
            'tools.sessions.httponly': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'log.access_file': "./server_handling/logs/access.log",
            'log.error_file': "./server_handling/logs/error.log",
            'log.screen': False,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../public/dist/'
        }
    }
    DirHandler.check_server_dirs()
    HashHandler.new_server_salt()
    cherrypy.quickstart(CryptoServer(), '/', conf)
