from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import cherrypy
import os
from hash_handler import HashHandler
import pymysql.cursors
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
        return open('../index.html')

    @cherrypy.expose()
    def sign(self):
        return open('../sign.html')

    @cherrypy.expose()
    def create_account(self, email, password):
        create_user_db(email, password)
        return open('../sign.html')

    @cherrypy.expose()
    def login_account(self, email, password):
        if db_check_user(email, password):
            return open('../index.html')
        else:
            return open('../sign.html')

    @cherrypy.expose()
    def file_upload(self, username, file):
        print(type(file))
        print(username)
        size = 0
        # Write the encrypted file
        with open('../profiles/000001/files/' + file.filename, 'wb') as f:
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

        key = Fernet.generate_key()

        key_file = open('../profiles/000001/keys/' + file.filename + '.key', 'wb')
        key_file.write(key)
        key_file.close()

        with open('../profiles/000001/files/' + file.filename, 'rb') as f:
            data_file = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data_file)

        with open('../profiles/000001/files/' + file.filename + '.encrypted', 'wb') as f:
            f.write(encrypted)
            return 'done'

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
    except:
        print("Error: unable to fetch data")
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
            sql = "SELECT email, password FROM users WHERE email = %s"
            cursor.execute(sql, (email, ))
            db.commit()
            result = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    finally:
        db.close()

    user_db_password = result[0]['password']

    if len(result) > 0:
        return HashHandler.verify_password(user_db_password, password)
    else:
        return False


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
    except:
        print("Error: unable to fetch data")
    finally:
        db.close()
    return True


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

