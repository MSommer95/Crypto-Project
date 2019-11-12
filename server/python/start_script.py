import os

import cherrypy
from jinja2 import Environment, FileSystemLoader

from server.python.db_connector import DbConnector
from server.python.dir_handler import DirHandler
from server.python.file_encryptor import FileEncryptor
from server.python.file_handler import FileHandler
from server.python.otp_handler import OtpHandler

ENV = Environment(loader=FileSystemLoader('/server/'))


class Index(object):
    # Index Call Function: Bearbeitet die Index Request der Website. Solange keine user_id gesetzt wurde, wird der User auf die Login Seite redirected
    # Überprüft die Session darauf, ob die 2fa aktiviert ist und ob der 2te Faktor schon bestätigt wurde
    @cherrypy.expose()
    def index(self):
        if cherrypy.session.get('user_id') is None:
            return open('../sign.html')
        else:
            if cherrypy.session.get('2fa_status') == 1:
                if cherrypy.session.get('2fa_verified') == 1:
                    return open('../index.html')
                else:
                    user_id = str(cherrypy.session.get('user_id'))
                    verified = DbConnector.db_check_otp_verified(user_id)
                    if verified:
                        cherrypy.session['2fa_verified'] = verified
                        return open('../index.html')
                    else:
                        return open('../sign.html')
            elif cherrypy.session.get('2fa_status') == 0:
                return open('../index.html')

    # Sign redirect
    @cherrypy.expose()
    def sign(self):
        return open('../sign.html')

    # create Funktion nimmt eine Emailadresse und Passwort entgegen und erstellt einen account in der DB + die
    # zugehörige Ordner Struktur
    @cherrypy.expose()
    def create_account(self, email, password):
        DirHandler.create_user_dir_structure(str(DbConnector.db_insert_user(email, password)))
        return open('../sign.html')

    # login Funktion nimmt Emailadresse und Passwort entgegen und überprüft, ob ein user existiert und ob das
    # passwort stimmt. Innere if Abfrage checked, welche settings der User aktiviert hat und initialisiert die
    # jeweiligen Session Variablen
    @cherrypy.expose()
    def login_account(self, email, password):
        user = DbConnector.db_check_user(email, password)
        user_count = len(user)
        if user_count > 0:
            cherrypy.session['user_id'] = user['id']
            cherrypy.session['2fa_verified'] = 0
            user_id = str(user['id'])
            user_settings = DbConnector.db_get_user_settings(user_id)

            if user_settings['2FA-Mail'] == 1:
                cherrypy.session['2fa_status'] = 1
                otp = OtpHandler.create_2fa(user_id)
                OtpHandler.send_otp_mail(otp, email)
                return 'Please send us your HOTP'

            elif user_settings['2FA-App'] == 1:
                cherrypy.session['2fa_status'] = 1
                otp = OtpHandler.create_2fa(user_id)
                OtpHandler.send_otp_app(otp, user_id)
                return 'Please send us your HOTP'

            else:
                cherrypy.session['2fa_status'] = 0
                DirHandler.check_user_dir_structure(user_id)
                return 'Send me to index'

        else:
            return 'Send me to sign'

    @cherrypy.expose()
    def logout_account(self):
        cherrypy.session.expire()
        return 'You are logged out'

    # verify Funktion überprüft, ob der eingegebene otp gültig ist (Innerhalb des Zeitraums und richtiger Code)
    @cherrypy.expose()
    def verify_otp(self, otp):
        user_id = str(cherrypy.session.get('user_id'))
        check_value = DbConnector.db_check_2fa(user_id, otp)
        if check_value:
            cherrypy.session['2fa_verified'] = 1
            DirHandler.check_user_dir_structure(user_id)
            return 'Varification valid'
        else:
            return 'Varification invalid'

    @cherrypy.expose()
    def verify_otp_app(self, otp, user_id):
        check_value = DbConnector.db_check_2fa(user_id, otp)
        if check_value:
            DbConnector.db_update_otp_verified(user_id)
            return 'Varification valid'
        else:
            return 'Varification invalid'

    @cherrypy.expose()
    def check_otp_verified(self):
        user_id = cherrypy.session.get('user_id')
        check_value = str(DbConnector.db_check_otp_verified(user_id))
        return check_value

    # upload Funktion nimmt eine file als Parameter entgegen und schreib sie in den unencrypted Fileordner des Users
    # nach dem Speichern der Datei wird die Datei verschlüsselt in den encrypted Ordner gelegt
    @cherrypy.expose()
    def file_upload(self, file):
        user_id = str(cherrypy.session.get('user_id'))
        FileHandler.write_file(user_id, file)

    # encryption Funktion nimmt einen Filename entgegen und verschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_encrypt(self, file_id, filename):
        user_id = str(cherrypy.session.get('user_id'))
        FileEncryptor.file_encryption(user_id, file_id, filename)

    # decryption Funktion nimmt einen Filename entgegen und entschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_decrypt(self, file_id, filename):
        user_id = str(cherrypy.session.get('user_id'))
        FileEncryptor.file_decryption(user_id, file_id, filename)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_files(self):
        user_id = str(cherrypy.session.get('user_id'))
        files = DbConnector.db_get_user_files(user_id)
        return files

    @cherrypy.expose()
    def users(self):
        return open('../users.html')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_users(self):
        users = DbConnector.db_get_users()
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        return users

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_devices(self):
        user_id = str(cherrypy.session.get('user_id'))
        devices = DbConnector.db_get_user_devices_by_user_id(user_id)
        return devices

    @cherrypy.expose()
    def insert_user_device(self, device_id, device_name):
        user_id = str(cherrypy.session.get('user_id'))
        db_connection_state = DbConnector.db_insert_user_devices(user_id, device_id, device_name)

        if db_connection_state == 'success':
            return 'Successfully inserted device'
        elif db_connection_state == 'failed':
            return 'Failed to insert device'

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def authenticate_app(self, email, password, device_id, device_name):
        print(device_id)
        user = DbConnector.db_check_user(email, password)
        user_count = len(user)
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'

        if user_count > 0:
            cherrypy.session['user_id'] = user['id']
            cherrypy.session['2fa_status'] = 0
            user_id = str(user['id'])
            user_settings = DbConnector.db_get_user_settings(user_id)

            if user_settings['2FA-App'] and user_settings['2FA-App'] == 1:
                devices = DbConnector.db_get_user_devices_by_user_id(user_id)
                print(str(devices))

                if len(devices) > 0 and any(x['device_id'] == device_id for x in devices):
                    cherrypy.session['2fa_status'] = 1
                    response = {'status': 200, 'message': 'Success'}
                    print('response', str(response))

                    return response
                else:
                    DbConnector.db_insert_user_devices(user_id, device_id, device_name)
                    response = {'status': 200, 'message': 'Device added'}
                    return response
            else:
                response = {'status': 403, 'message': 'App auth inactive'}
                return response
        else:
            response = {'status': 403, 'message': 'No such user found or password wrong'}
            return response

    @cherrypy.expose()
    def request_otp_app(self, device_id):
        device = DbConnector.db_get_user_devices_by_device_id(device_id)
        user_id = str(device[0]['user_id'])
        user_settings = DbConnector.db_get_user_settings(user_id)

        if user_settings['2FA-App'] and user_settings['2FA-App'] == 1:
            otp = OtpHandler.create_2fa(user_id)
            return otp


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.sessions.timeout': 20
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../public'
        }
    }
    cherrypy.quickstart(Index(), '/', conf)
