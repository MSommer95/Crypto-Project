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
from user_class import User
import pymysql.cursors
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('/server/'))

params = {'dbname': 'project',
          'user': 'root',
          'password': 'HMpXB44P',
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
    def register(self, firstname, lastname, username, email, password):

        user_instance = User(firstname, lastname, username, email)
        user_instance.create_user_db(password)

        return

    @cherrypy.expose()
    def sign_in(self, password, user_credentials='default'):

        if '@' in user_credentials:
            check_for_email = True
        else:
            check_for_email = False

        print(check_for_email)
        print(password)

        return

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
            '''.format(file.filename, size, file.content_type, data)

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
        return db_getusers()


def db_getusers():
    tmpl = ENV.get_template('users.html')
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
            print(results)
    except:
        print("Error: unable to fetch data")
    finally:
        db.close()

    return tmpl.render(results[0])


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

