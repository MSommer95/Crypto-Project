from cryptography.fernet import Fernet
import cherrypy
import os
import base64
import MySQLdb
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
