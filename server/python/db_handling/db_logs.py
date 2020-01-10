import logging
import time

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBlogs:

    @staticmethod
    def insert(user_id):
        db = DBconnector.connect()
        ts = int(time.time())
        try:
            with db.cursor() as cursor:
                sql = 'INSERT INTO login_logs (user_id, counter, timestamp) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, 0, ts))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def get_login_log(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM login_logs WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return result

    @staticmethod
    def update_login_log(user_id, counter):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE login_logs SET counter = %s WHERE user_id = %s'
                cursor.execute(sql, (counter, user_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def delete_login_log(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'DELETE FROM login_logs WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
            return 'Something went wrong'
        else:
            return 'Successful login_logs deleted'
        finally:
            db.close()

    @staticmethod
    def set_is_send(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE login_logs SET is_send = 1 WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
