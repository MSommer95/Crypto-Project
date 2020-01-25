import pymysql.cursors


class DBconnector:

    @staticmethod
    def connect():
        params = {'dbname': 'project',
                  'user': 'root',
                  'password': 'HMpXB44P',
                  'dbhost': '127.0.0.1',
                  'charset': 'utf8mb4'}

        db = pymysql.connect(host=params['dbhost'],
                             user=params['user'],
                             password=params['password'],
                             db=params['dbname'],
                             charset=params['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
        return db
