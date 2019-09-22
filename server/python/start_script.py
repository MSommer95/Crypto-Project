from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('/server/'))

params = {'dbname': 'project',
          'user': 'root',
          'password': 'HMpXB44P',
          'dbhost': '127.0.0.1'}


class Index(object):

    @cherrypy.expose()
    def index(self):
        return open('../index.html')

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
    def public_key_exchange(self):

        parameters = dh.generate_parameters(generator=2, key_size=1028, backend=default_backend())
        private_key = parameters.generate_private_key()
        peer_public_key = parameters.generate_private_key().public_key()
        shared_key = private_key.exchange(peer_public_key)

        derived_key = HKDF(algorithm = hashes.SHA256(),length = 32,salt = None,info = b'handshake data',backend = default_backend()).derive(shared_key)

        return derived_key

    '''    @cherrypy.expose()
    def users(self):
        return db_getusers()


def db_getusers():
    tmpl = ENV.get_template('users.html')
    db = MySQLdb.connect(params['dbhost'],
                         params['user'],
                         params['password'],
                         params['dbname'])
    cursor = db.cursor()
    sql = "SELECT * FROM users"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        user = {}
        user['id'] = results[0][0]
        user['email'] = results[0][1]
        user['password'] = results[0][2]
    except:
        print("Error: unable to fetch data")

    return tmpl.render(user)
'''


def forge_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    pem_priv = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword'))

    with open('../private_key/private_key.pem', 'wb') as f:
        f.write(pem_priv)
        f.close()

    public_key = private_key.public_key()
    pem_pub = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open('../public/public_key/public_key.pem', 'wb') as f:
        f.write(pem_pub)
        f.close


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
    forge_key()
    cherrypy.quickstart(Index(), '/', conf)

