import os

import cherrypy
from server.python.db_connector import DbConnector
from server.python.otp_handler import OtpHandler
from server.python.file_encryptor import FileEncryptor
from server.python.dir_handler import DirHandler
from jinja2 import Environment, FileSystemLoader

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
                if cherrypy.session.get('2fa_varified') == 1:
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
        db = DbConnector.create_db_connection()
        DirHandler.create_dirs(str(DbConnector.create_user_db(db, email, password)))
        return open('../sign.html')

    # login Funktion nimmt Emailadresse und Passwort entgegen und überprüft, ob ein user existiert und ob das
    # passwort stimmt. Innere if Abfrage checked, welche settings der User aktiviert hat und initialisiert die
    # jeweiligen Session Variablen
    @cherrypy.expose()
    def login_account(self, email, password):
        db = DbConnector.create_db_connection()
        user = DbConnector.db_check_user(db, email, password)
        check_log_status = False
        if len(user) > 0:
            check_log_status = True
        if check_log_status:
            db = DbConnector.create_db_connection()
            user_settings = DbConnector.get_user_settings(db, user['id'])
            if user_settings['2FA'] == 1:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 1
                cherrypy.session['2fa_varified'] = 0
                otp = OtpHandler.create_2FA(user['id'], email)

                # TODO if mail activated
                OtpHandler.send_otp_mail(otp, email)
                # TODO elif app activated
                # TODO send_app(otp, params)

                return 'Please send us your HOTP'
            else:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 0
                DirHandler.check_for_dirs(str(cherrypy.session['user_id']))
                return 'Send me to index'
        else:
            return 'Send me to sign'

    # verify Funktion überprüft, ob der eingegebene otp gültig ist (Innerhalb des Zeitraums und richtiger Code)
    @cherrypy.expose()
    def verify_otp(self, otp):
        db = DbConnector.create_db_connection()
        check_value = DbConnector.check_2FA(db, cherrypy.session.get('user_id'), otp)
        if check_value:
            cherrypy.session['2fa_varified'] = 1
            DirHandler.check_for_dirs(str(cherrypy.session['user_id']))
            return 'Varification valid'
        else:
            return 'Varification invalid'

    # upload Funktion nimmt eine file als Parameter entgegen und schreib sie in den unencrypted Fileordner des Users
    # nach dem Speichern der Datei wird die Datei verschlüsselt in den encrypted Ordner gelegt
    @cherrypy.expose()
    def file_upload(self, file):
        print(type(file))
        size = 0
        # Write the encrypted file
        with open('../storage/users/%s/files/unencrypted/%s' % (str(cherrypy.session['user_id']), file.filename), 'wb') as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)
            f = '''
            File received.
            Filename: {}
            Length: {}
            Mime-type: {}
            .format(file.filename, size, file.content_type, data)'''

            print(f)

        FileEncryptor.file_encryption(str(cherrypy.session['user_id']), file)

    # decryption Funktion nimmt einen Filename entgegen und entschlüsselt die jeweilige Datei
    @cherrypy.expose()
    def file_decrypt(self, filename):
        print(filename)
        FileEncryptor.file_decryption(str(cherrypy.session.get('user_id')), filename)

    @cherrypy.expose()
    def users(self):
        return open('../users.html')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def get_users(self):
        db = DbConnector.create_db_connection()
        users = DbConnector.db_get_users(db)
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        return users


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
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
