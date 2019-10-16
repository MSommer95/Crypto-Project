import logging
import os
import secrets
import time
import cherrypy
import pymysql.cursors
from email_sender import EmailSender
from file_encryptor import FileEncryptor
from hash_handler import HashHandler
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('/server/'))

params = {'dbname': 'project',
          'user': 'root',
          'password': 'HMpXB44P',  # root
          'dbhost': '127.0.0.1',
          'charset': 'utf8mb4'}


class Index(object):

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
        create_dirs(str(create_user_db(email, password)))
        return open('../sign.html')

    @cherrypy.expose()
    def login_account(self, email, password):
        user = db_check_user(email, password)
        check_log_status = False
        if len(user) > 0:
            check_log_status = True
        if check_log_status:
            user_settings = get_user_settings(user['id'])
            if user_settings['description'] == 1:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 1
                cherrypy.session['2fa_varified'] = 0
                create_2FA(user['id'], email)
                return 'Please send us your HOTP'
            else:
                cherrypy.session['user_id'] = user['id']
                cherrypy.session['2fa_status'] = 0
                return 'Send me to index'
        else:
            return 'Send me to sign'

    @cherrypy.expose()
    def verify_hotp(self, hotp):
        check_value = check_2FA(cherrypy.session.get('user_id'), hotp)
        if check_value:
            cherrypy.session['2fa_varified'] = 1
            return 'Varification valid'
        else:
            return 'Varification invalid'

    @cherrypy.expose()
    def file_upload(self, file):
        print(type(file))
        size = 0
        # Write the encrypted file
        with open('../storage/users/%s/files/%s' % (str(cherrypy.session['user_id']), file.filename), 'wb') as f:
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
        users = db_get_users()
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        return users


def db_get_users():
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            db.commit()
            results = cursor.fetchall()
    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()

    return results


def db_check_user(email, password):
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor() as cursor:
            sql = "SELECT id, email, password FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            db.commit()
            result = cursor.fetchall()
    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()

    user_db_password = result[0]['password']

    if len(result) > 0 and HashHandler.verify_password(user_db_password, password):
        return result[0]
    else:
        return []


def get_user_settings(user_id):
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor() as cursor:
            sql = "SELECT t2.description, setting_value FROM user_setting as t1 JOIN settings as t2 ON t1.settings_id = t2.id WHERE t1.user_id = %s"
            cursor.execute(sql, (user_id,))
            db.commit()
            result = cursor.fetchall()
            settings = {}
            for entry in result:
                settings["description"] = int(entry["setting_value"])

    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()

    return settings


def update_user_2fa(user_id, hotp):
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor() as cursor:
            ts = int(time.time())
            sql = "DELETE FROM user_otp WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            sql = "INSERT INTO user_otp (user_id, current_otp, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, hotp, ts))
            db.commit()
    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()


def create_user_db(email, password):
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    hashed_password = HashHandler.hash_password(password)
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
            cursor.execute(sql, (email, hashed_password))
            db.commit()
            sql = "SELECT id FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            db.commit()
            result = cursor.fetchall()
            sql = "INSERT INTO user_setting (user_id, settings_id, setting_value) VALUES (%s, 1, 1)"
            cursor.execute(sql, (result[0]['id'],))
            db.commit()
    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()
    return result[0]['id']


def create_2FA(user_id, email):
    hotp_value = ''
    for x in range(8):
        hotp_value += str(secrets.randbelow(9))

    update_user_2fa(user_id, hotp_value)
    message = 'Your HOTP: %s' % hotp_value
    EmailSender.send_mail(message, '2-Faktor-Auth', email)
    return


def check_2FA(user_id, hotp):
    db = pymysql.connect(host=params['dbhost'],
                         user=params['user'],
                         password=params['password'],
                         db=params['dbname'],
                         charset=params['charset'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor() as cursor:
            sql = "SELECT current_otp FROM user_otp WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            db.commit()
            result = cursor.fetchall()
    except pymysql.MySQLError as e:
        logging.error(e)
    finally:
        db.close()

    db_hotp = result[0]['current_otp']

    if db_hotp == hotp:
        return True
    else:
        return False


def create_dirs(user_id):
    path = '../storage/users/'
    sub_dirs = ['/keys', '/files', '/others']
    try:
        os.mkdir(path + user_id)
    except OSError:
        print('Creating Dir %s failed' % path)
    else:
        print('Successfully created Dir %s' % path)
        for dirs in sub_dirs:
            try:
                os.mkdir(path + user_id + dirs)
            except OSError:
                print('Creating Dir %s failed' % path)
            else:
                print('Successfully created Dir %s' % path + user_id + dirs)


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
