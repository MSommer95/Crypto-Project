import base64
import os

import cherrypy
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader

from server.python.comm_handling.qr_handler import QRHandler
from server.python.db_handling.db_devices import DBdevices
from server.python.db_handling.db_files import DBfiles
from server.python.db_handling.db_otp import DBotp
from server.python.db_handling.db_users import DBusers
from server.python.db_handling.hash_handler import HashHandler
from server.python.file_handling.file_encryptor import FileEncryptor
from server.python.file_handling.file_handler import FileHandler
from server.python.otp_handling.otp_handler import OtpHandler
from server.python.otp_handling.second_factor_handling import SecondFactorHandler
from server.python.server_handling.dir_handler import DirHandler
from server.python.server_handling.login_log_handler import LLogHandler

ENV = Environment(loader=FileSystemLoader('/server/'))


class Index(object):
    # Index Call Function: Bearbeitet die Index Request der Website. Solange keine user_id gesetzt wurde,
    # wird der User auf die Login Seite redirected Überprüft die Session darauf, ob die 2fa aktiviert ist und ob der
    # 2te Faktor schon bestätigt wurde
    @cherrypy.expose()
    def index(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            return open('../public/dist/index.html')
        else:
            cherrypy.response.status = 401
            return open('../public/dist/sign.html')

    # Sign redirect
    @cherrypy.expose()
    def sign(self):
        return open('../public/dist/sign.html')

    # create Funktion nimmt eine Emailadresse und Passwort entgegen und erstellt einen account in der DB + die
    # zugehörige Ordner Struktur
    @cherrypy.expose()
    def create_account(self, email, password):
        DirHandler.create_user_dirs(str(DBusers.insert_user(email, password)))
        return open('../public/dist/sign.html')

    # login Funktion nimmt Emailadresse und Passwort entgegen und überprüft, ob ein user existiert und ob das
    # passwort stimmt. Innere if Abfrage checked, welche settings der User aktiviert hat und initialisiert die
    # jeweiligen Session Variablen
    @cherrypy.expose()
    def login_account(self, email, password):
        user_id = DBusers.get_user_id(email)[0]['id']
        if user_id:
            user_logs = LLogHandler.check_login_logs(user_id)
            login_trys = LLogHandler.count_trys(user_id, user_logs, email)
            if login_trys:
                user = DBusers.check_user(email, password)
                user_count = len(user)
                if user_count > 0:
                    cherrypy.session['user_id'] = user['id']
                    cherrypy.session['user_mail'] = user['email']
                    cherrypy.session['2fa_verified'] = 0
                    user_id = str(user['id'])
                    user_settings = DBusers.get_user_settings(user_id)
                    DirHandler.check_user_dirs(user_id)
                    if user_settings['2FA-Mail'] == 1:
                        cherrypy.session['2fa_status'] = 1
                        cherrypy.session['otp_option'] = 1
                        otp = OtpHandler.create_otp(user_id)
                        DBotp.insert(user_id, otp)
                        OtpHandler.send_otp_mail(email, otp)
                        return 'Please send us your OTP'
                    elif user_settings['2FA-App'] == 1:
                        cherrypy.session['2fa_status'] = 1
                        cherrypy.session['otp_option'] = 2
                        otp = OtpHandler.create_otp(user_id)
                        DBotp.insert(user_id, otp)
                        OtpHandler.send_otp_app(user_id, otp)
                        return 'Please send us your OTP'
                    else:
                        cherrypy.session['2fa_status'] = 0
                        return 'Send me to index'
                else:
                    cherrypy.response.status = 403
                    return 'Wrong data. Try again.'
            else:
                cherrypy.response.status = 418  # 429
                return 'Too many Trys. Try again in a minute.'

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
        cherrypy.session.delete()
        return 'You are logged out'

    # verify Funktion überprüft, ob der eingegebene otp gültig ist (Innerhalb des Zeitraums und richtiger Code)
    @cherrypy.expose()
    def verify_otp(self, otp):
        user_id = check_session_value('user_id')
        if user_id:
            user_id = str(user_id)
            check_value = DBotp.check_current(user_id, otp)
            if check_value:
                cherrypy.session['2fa_verified'] = 1
                DirHandler.check_user_dirs(user_id)
                return 'Verification valid'
            else:
                cherrypy.response.status = 403
                return 'Verification invalid'
        else:
            return unauthorized_response()

    # Funktion zur Überprüfung eines per App gesendeten One-Time-Passwords, gültige Passwörter sind unbenutzt udn
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
        user_id = check_session_value('user_id')
        # TODO: Potenzielle Schwachstelle wenn Eve password und email kennt und login versucht und Bob den
        #   otp via app bestätigt und damit die varification auf 1 setzt
        if user_id:
            check_value = DBotp.check_verification(user_id)
            if check_value:
                cherrypy.session['2fa_verified'] = 1
            return str(check_value)
        else:
            return unauthorized_response()

    # upload Funktion nimmt eine file als Parameter entgegen und schreib sie in den unencrypted Fileordner des Users
    # nach dem Speichern der Datei wird die Datei verschlüsselt in den encrypted Ordner gelegt
    @cherrypy.expose()
    def file_upload(self, file):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            FileHandler.write_file(user_id, file)
            return open('../public/dist/index.html')
        else:
            return open('../public/dist/sign.html')

    # Funktion zum Herunterladen einer bestehenden Datei des Nutzers auf dem Server
    @cherrypy.expose()
    def file_download(self, file_path):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            user_path = '../storage/users/%s' % user_id
            absolute_file_path = os.path.abspath(user_path + file_path)
            return serve_file(absolute_file_path, disposition="attachment")
        else:
            return open('../public/dist/sign.html')

    # encryption Funktion nimmt einen Filename entgegen und verschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_encrypt(self, file_id, file_name):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            return FileEncryptor.encryption(user_id, file_id, file_name)
        else:
            return unauthorized_response()

    # decryption Funktion nimmt einen Filename entgegen und entschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_decrypt(self, file_id, file_name):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            file_name = file_name.strip('.encrypted')
            return FileEncryptor.decryption(user_id, file_id, file_name)
        else:
            return unauthorized_response()

    # Funktion zur Änderung einer bestehenden hochgeladenen Datei des Nutzers
    @cherrypy.expose()
    def file_update(self, file_id, file_description, path, file_name, is_encrypted):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            if int(is_encrypted):
                new_path = '/files/encrypted/%s' % file_name
            else:
                new_path = '/files/unencrypted/%s' % file_name
            DBfiles.update_file(user_id, file_id, file_name, file_description, new_path)
            return FileHandler.change_file_name(user_id, file_id, file_name, path, is_encrypted)
        else:
            return unauthorized_response()

    # Funktion zum Entfernen einer hochgeladenen Datei des Nutzers
    @cherrypy.expose()
    def file_delete(self, file_id, path, is_encrypted):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            return FileHandler.delete_file(user_id, file_id, path, is_encrypted)
        else:
            return unauthorized_response()

    # Funktion zum Auslesen aller hochgeladenen Dateien des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_files(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            files = DBfiles.get_files(user_id)
            return files
        else:
            return unauthorized_response()

    # Funktion zum Auslesen aller bereits genutzten OTP's des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_used_otps(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            used_otps = DBotp.get_used(user_id)
            return used_otps
        else:
            return unauthorized_response()

    # Funktion zum Auslesen aller registrierten Nutzer-Devices
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_devices(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            devices = DBdevices.get_by_user_id(user_id)
            return devices
        else:
            return unauthorized_response()

    # Funktion zum Hinzufügen eines neuen Nutzer-Devices, genutzt für Authentifikation per App als zweiten Faktor
    @cherrypy.expose()
    def insert_user_device(self, device_id, device_name, user_id):
        if not user_id:
            user_id = check_session_value('user_id')
            if check_for_auth(user_id):
                user_id = str(user_id)
            else:
                return unauthorized_response()
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
    def delete_user_device(self, device_id):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            DBdevices.delete(device_id, user_id)
            deleted_message = 'Device was deleted. \n' + SecondFactorHandler.check_for_active_device(user_id)
            return deleted_message
        else:
            return unauthorized_response()

    # Funktion zum Aktivieren eines bereits existenten Devices für die 2-Faktor-Authentifikation, es kann nur jeweils
    # ein Device gleichzeitig aktiver zweiter Faktor sein
    @cherrypy.expose()
    def activate_user_device(self, device_id):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            DBdevices.deactivate_all(user_id)
            return SecondFactorHandler.activate_device(user_id, device_id)
        else:
            return unauthorized_response()

    # Funktion zum Deaktivieren eines aktiven 2-Faktor-Devices des Nutzers
    @cherrypy.expose()
    def deactivate_user_device(self, device_id):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            deactived_message = SecondFactorHandler.deactivate_device(user_id, device_id)
            deactivae_addition = SecondFactorHandler.check_for_active_device(user_id)
            return deactived_message + ' ' + deactivae_addition
        else:
            return unauthorized_response()

    # Funktion zum Auslesen der gewählten 2-Faktor-Eistellungen des Nutzers
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_settings(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            user_settings = DBusers.get_user_settings(user_id)
            user = DBusers.get_user(user_id)
            user_settings['email'] = user[0]['email']
            return user_settings
        else:
            return unauthorized_response()

    # Funktion zum Ändern des Passworts oder der Email eines Nutzers
    @cherrypy.expose()
    def update_account_info(self, email, password):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            user_mail = check_session_value('user_mail')
            email_change_status = ''
            password_change_status = ''
            if not user_mail == email:
                email_change_status = DBusers.update_email(user_id, email)
            if not password == '':
                password_change_status = DBusers.update_password(user_id, password)
            return email_change_status + password_change_status
        else:
            return unauthorized_response()

    # Funktion zum anpassen der 2-Faktor-Einstellungen des Nutzers, bei Aktivierung der 2-Faktor Authentifikation
    # wird ein einmaliges Token zum Zurücksetzen der Einlstellungen generiert und in der Datenbank gespeichert
    @cherrypy.expose()
    def update_settings_sec_fa(self, sec_fa, sec_fa_email, sec_fa_app):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            if sec_fa_email == 'true' and sec_fa_app == 'true':
                return 'Please dont try to check more then one 2FA option'
            else:
                if sec_fa == 'true':
                    if sec_fa_app == 'true':
                        devices = DBdevices.get_by_user_id(user_id)
                        if len(devices) == 0:
                            return 'No active device found! Please register one first and active it'

                    DBusers.set_second_factor_option(user_id, 1, int(sec_fa_email == 'true'))
                    DBusers.set_second_factor_option(user_id, 2, int(sec_fa_app == 'true'))
                    token = HashHandler.create_token(user_id)
                    return 'Successfully changed the second factor, use token: "%s" to reset your 2FA settings ' % token
                else:
                    DBusers.set_second_factor_option(user_id, 1, 0)
                    DBusers.set_second_factor_option(user_id, 2, 0)
                    return 'Successfully disabled second factor'
        else:
            return unauthorized_response()

    # Funktion zum zurücksetzen der 2-Faktor Authentifizierung mittels Token, falls Nutzer Zugang zum
    # Authentifikationsmedium verliert
    @cherrypy.expose()
    def reset_settings_sec_fa(self, token):
        user_id = check_session_value('user_id')
        if user_id:
            if HashHandler.check_token(user_id, token):
                DBusers.set_second_factor_option(user_id, 1, 0)
                DBusers.set_second_factor_option(user_id, 2, 0)
                return 'Successfully disabled second factor. Please login again.'
            else:
                cherrypy.response.status = 403
                return 'Token mismatch'
        else:
            return unauthorized_response()

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
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            user_mail = check_session_value('user_mail')
            otp_option = check_session_value('otp_option')
            otp = OtpHandler.create_otp(user_id)
            DBotp.insert(user_id, otp)
            if otp_option == 1:
                OtpHandler.send_otp_mail(user_mail, otp)
            elif otp_option == 2:
                OtpHandler.send_otp_app(user_id, otp)
            return 'New OTP send'

    # Funktion zum erstellen eines QR-Code Bildes auf Basis der Daten user_id und otp im JSON Format, kann in der App
    # gescanned werden um Registrierung und Login zu vereinfachen
    @cherrypy.expose()
    def request_qr(self):
        user_id = check_session_value('user_id')
        if check_for_auth(user_id):
            user_id = str(user_id)
            otp = OtpHandler.create_otp(user_id)
            img_string = QRHandler.create_qr_image(user_id, otp)
            cherrypy.response.headers['Content-Type'] = "image/png"
            return base64.b64encode(img_string)
        else:
            return unauthorized_response()

    @cherrypy.expose()
    def request_top_password(self):
        return open('../storage/other/top500passwords')


def check_session_value(value):
    if cherrypy.session.get(value):
        return cherrypy.session.get(value)
    else:
        return False


def check_for_auth(user_id):
    if check_session_value('2fa_status'):
        return check_session_value('2fa_verified')
    else:
        return user_id


def unauthorized_response():
    cherrypy.response.status = 401
    return 'Access denied: Unauthorized'


if __name__ == '__main__':
    os.chdir('../')


    @cherrypy.tools.register('before_finalize', priority=60)
    def secureheaders():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        # headers['Content-Security-Policy'] = "default-src 'self';"


    conf = {
        '/': {
            'tools.secureheaders.on': True,
            'tools.sessions.on': True,
            'tools.sessions.timeout': 20,
            # TODO: Only if HTTPS is activated 'tools.sessions.secure': True,
            'tools.sessions.httponly': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'log.access_file': "./server_handling/logs/access.log",
            'log.error_file': "./server_handling/logs/error.log",
            'log.screen': False,
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../public/dist/'
        }
    }
    DirHandler.check_server_dirs()
    cherrypy.quickstart(Index(), '/', conf)
