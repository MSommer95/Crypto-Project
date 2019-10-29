import os
import secrets

import cherrypy
from server.python.db_connector import DbConnector
from server.python.email_sender import EmailSender
from server.python.file_encryptor import FileEncryptor
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('/server/'))


class Index(object):
    ### Index Call Function: Bearbeitet die Index Request der Website. Solange keine user_id gesetzt wurde, wird der User auf die Login Seite
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

    @cherrypy.expose()
    def sign(self):
        return open('../sign.html')

    @cherrypy.expose()
    def create_account(self, email, password):
        db = DbConnector.create_db_connection()
        create_dirs(str(DbConnector.create_user_db(db, email, password)))
        return open('../sign.html')

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
            if user_settings['description'] == 1:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 1
                cherrypy.session['2fa_varified'] = 0
                create_2FA(user['id'], email)
                return 'Please send us your HOTP'
            else:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 0
                check_for_dirs(str(cherrypy.session['user_id']))
                return 'Send me to index'
        else:
            return 'Send me to sign'

    @cherrypy.expose()
    def verify_hotp(self, hotp):
        db = DbConnector.create_db_connection()
        check_value = DbConnector.check_2FA(db, cherrypy.session.get('user_id'), hotp)
        if check_value:
            cherrypy.session['2fa_varified'] = 1
            check_for_dirs(str(cherrypy.session['user_id']))
            return 'Varification valid'
        else:
            return 'Varification invalid'

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


def create_2FA(user_id, email):
    hotp_value = ''
    for x in range(8):
        hotp_value += str(secrets.randbelow(9))
    db = DbConnector.create_db_connection()
    hotp_used = DbConnector.check_for_used_otp(db, user_id, hotp_value)

    if hotp_used:
        create_2FA(user_id, email)
        return
    else:
        db = DbConnector.create_db_connection()
        DbConnector.update_user_2fa(db, user_id, hotp_value)
        message = 'Your HOTP: %s' % hotp_value
        EmailSender.send_mail(message, '2-Faktor-Auth', email)
        return


def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print('Creating Dir %s failed' % path)
    else:
        print('Successfully created Dir %s' % path)


def create_dirs(user_id):
    path = '../storage/users/'
    sub_dirs = ['/keys', '/files', '/others']
    sub_dirs_files = ['/unencrypted', '/encrypted']
    try:
        os.mkdir(path + user_id)
    except OSError:
        print('Creating Dir %s failed' % path)
    else:
        print('Successfully created Dir %s' % path)
        for dirs in sub_dirs:
            make_dir(path + user_id + dirs)
        for dirs in sub_dirs_files:
            make_dir(path + user_id + '/files' + dirs)


def check_for_dirs(user_id):
    base_path = '../storage/users/%s' % user_id
    paths = [
        '/files',
        '/keys',
        '/others'
    ]
    inner_paths = [
        '/unencrypted',
        '/encrypted'
    ]

    if os.path.isdir(base_path):
        if os.path.isdir(base_path + paths[0]):
            for path in inner_paths:
                if not os.path.isdir(base_path + paths[0] + path):
                    make_dir(base_path + paths[0] + path)
        else:
            make_dir(base_path + paths[0])
            for dirs in inner_paths:
                make_dir(base_path + paths[0] + dirs)

        for x in range(1, len(paths)):
            if not os.path.isdir(base_path + paths[x]):
                make_dir(base_path + paths[x])
    else:
        create_dirs(user_id)


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
