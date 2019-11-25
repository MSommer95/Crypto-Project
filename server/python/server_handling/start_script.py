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
from server.python.file_handling.file_encryptor import FileEncryptor
from server.python.file_handling.file_handler import FileHandler
from server.python.otp_handling.otp_handler import OtpHandler
from server.python.otp_handling.second_factor_handling import SecondFactorHandler
from server.python.server_handling.dir_handler import DirHandler

ENV = Environment(loader=FileSystemLoader('/server/'))


class Index(object):
    # Index Call Function: Bearbeitet die Index Request der Website. Solange keine user_id gesetzt wurde, wird der User auf die Login Seite redirected
    # Überprüft die Session darauf, ob die 2fa aktiviert ist und ob der 2te Faktor schon bestätigt wurde
    @cherrypy.expose()
    def index(self):
        if cherrypy.session.get('user_id') is None:
            return open('../public/dist/sign.html')
        else:
            if cherrypy.session.get('2fa_status') == 1:
                if cherrypy.session.get('2fa_verified') == 1:
                    return open('../public/dist/index.html')
                else:
                    user_id = str(cherrypy.session.get('user_id'))
                    verified = DBotp.check_otp_verified(user_id)
                    if verified:
                        cherrypy.session['2fa_verified'] = verified
                        return open('../public/dist/index.html')
                    else:
                        return open('../public/dist/sign.html')
            elif cherrypy.session.get('2fa_status') == 0:
                return open('../public/dist/index.html')

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
        user = DBusers.check_user(email, password)
        user_count = len(user)
        if user_count > 0:
            cherrypy.session['user_id'] = user['id']
            cherrypy.session['2fa_verified'] = 0
            user_id = str(user['id'])
            user_settings = DBusers.get_user_settings(user_id)
            DirHandler.check_user_dirs(user_id)
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
                return 'Send me to index'

        else:
            return 'Send me to sign'

    @cherrypy.expose()
    def logout_account(self):
        cherrypy.session.delete()
        return 'You are logged out'

    # verify Funktion überprüft, ob der eingegebene otp gültig ist (Innerhalb des Zeitraums und richtiger Code)
    @cherrypy.expose()
    def verify_otp(self, otp):
        user_id = str(cherrypy.session.get('user_id'))
        check_value = DBotp.check_current_otp(user_id, otp)
        if check_value:
            cherrypy.session['2fa_verified'] = 1
            DirHandler.check_user_dirs(user_id)
            return 'Verification valid'
        else:
            return 'Verification invalid'

    @cherrypy.expose()
    def verify_otp_app(self, otp, user_id):
        check_value = DBotp.check_current_otp(user_id, otp)
        if check_value:
            DBotp.update_otp_verified(user_id)
            return 'Verification valid'
        else:
            return 'Verification invalid'

    @cherrypy.expose()
    def check_otp_verified(self):
        user_id = cherrypy.session.get('user_id')
        check_value = str(DBotp.check_otp_verified(user_id))
        return check_value

    # upload Funktion nimmt eine file als Parameter entgegen und schreib sie in den unencrypted Fileordner des Users
    # nach dem Speichern der Datei wird die Datei verschlüsselt in den encrypted Ordner gelegt
    @cherrypy.expose()
    def file_upload(self, file):
        user_id = str(cherrypy.session.get('user_id'))
        FileHandler.write_file(user_id, file)
        return open('../public/dist/index.html')

    @cherrypy.expose()
    def file_download(self, file_path):
        user_id = str(cherrypy.session.get('user_id'))
        user_path = '../storage/users/%s' % user_id
        absolute_file_path = os.path.abspath(user_path + file_path)
        return serve_file(absolute_file_path, disposition="attachment")

    # encryption Funktion nimmt einen Filename entgegen und verschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_encrypt(self, file_id, file_name):
        user_id = str(cherrypy.session.get('user_id'))
        return FileEncryptor.encryption(user_id, file_id, file_name)

    # decryption Funktion nimmt einen Filename entgegen und entschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_decrypt(self, file_id, file_name):
        user_id = str(cherrypy.session.get('user_id'))
        file_name = file_name.strip('.encrypted')
        return FileEncryptor.decryption(user_id, file_id, file_name)

    @cherrypy.expose()
    def file_update(self, file_id, file_description, path, file_name, is_encrypted):
        user_id = str(cherrypy.session.get('user_id'))
        if int(is_encrypted):
            new_path = '/files/encrypted/%s' % file_name
        else:
            new_path = '/files/unencrypted/%s' % file_name
        DBfiles.update_user_file(user_id, file_id, file_name, file_description, new_path)
        return FileHandler.change_file_name(user_id, file_id, file_name, path, is_encrypted)

    @cherrypy.expose()
    def file_delete(self, file_id, path, is_encrypted):
        user_id = str(cherrypy.session.get('user_id'))
        return FileHandler.delete_file(user_id, file_id, path, is_encrypted)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_files(self):
        user_id = str(cherrypy.session.get('user_id'))
        files = DBfiles.get_user_files(user_id)
        return files

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_used_otps(self):
        user_id = str(cherrypy.session.get('user_id'))
        used_otps = DBotp.get_used_otps(user_id)
        return used_otps

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_user_devices(self):
        user_id = str(cherrypy.session.get('user_id'))
        devices = DBdevices.get_devices_by_user_id(user_id)
        return devices

    @cherrypy.expose()
    def insert_user_device(self, device_id, device_name):
        user_id = str(cherrypy.session.get('user_id'))
        db_connection_state = DBdevices.insert_user_device(user_id, device_id, device_name)

        if db_connection_state == 'success':
            return 'Successfully inserted device'
        elif db_connection_state == 'failed':
            return 'Failed to insert device'

    #  ToDo: filter for active device to allow login
    @cherrypy.expose()
    def delete_user_device(self, device_id):
        user_id = str(cherrypy.session.get('user_id'))
        DBdevices.delete_device(device_id, user_id)
        deleted_message = 'Device was deleted. \n' + SecondFactorHandler.check_for_active_device(user_id)
        return deleted_message

    @cherrypy.expose()
    def activate_user_device(self, device_id):
        user_id = str(cherrypy.session.get('user_id'))
        DBdevices.deactivate_all_user_devices(user_id)
        return SecondFactorHandler.activate_device(user_id, device_id)

    @cherrypy.expose()
    def deactivate_user_device(self, device_id):
        user_id = str(cherrypy.session.get('user_id'))
        deactived_message = SecondFactorHandler.deactivate_device(user_id, device_id)
        deactivae_addition = SecondFactorHandler.check_for_active_device(user_id)
        return deactived_message + ' ' + deactivae_addition

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
                devices = DBdevices.get_devices_by_user_id(user_id)
                print(str(devices))

                if len(devices) > 0 and any(x['device_id'] == device_id for x in devices):
                    cherrypy.session['2fa_status'] = 1
                    response = {'status': 200, 'message': 'Success'}
                    print('response', str(response))

                    return response
                else:
                    DBdevices.insert_user_device(user_id, device_id, device_name)
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
        device = DBdevices.get_devices_by_device_id(device_id)
        user_id = str(device[0]['user_id'])
        user_settings = DBusers.get_user_settings(user_id)
        if user_settings['2FA-App'] and user_settings['2FA-App'] == 1:
            otp = OtpHandler.create_2fa(user_id)
            return otp

    @cherrypy.expose()
    def request_qr(self):
        user_id = str(cherrypy.session.get('user_id'))
        otp = OtpHandler.create_2fa(user_id)
        img_string = QRHandler.create_qr_image(user_id, otp)
        cherrypy.response.headers['Content-Type'] = "image/png"
        return base64.b64encode(img_string)


if __name__ == '__main__':
    os.chdir('../')
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.sessions.timeout': 20,
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
