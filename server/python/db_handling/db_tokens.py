import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBtokens:

    @staticmethod
    def insert(user_id, token, reset_case):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                if reset_case == 1:
                    sql = 'DELETE FROM user_tokens WHERE user_id = %s AND reset_case = %s'
                    cursor.execute(sql, (user_id, reset_case))
                sql = 'INSERT INTO user_tokens (user_id, token, reset_case) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, token, reset_case))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def insert_auth_token(user_id, token, session_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'DELETE FROM auth_tokens WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                sql = 'INSERT INTO auth_tokens (user_id, token, session_id) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, token, session_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def get(user_id, reset_case):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT token FROM user_tokens WHERE user_id = %s AND reset_case = %s'
                cursor.execute(sql, (user_id, reset_case))
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return results

    @staticmethod
    def get_auth_token(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT token, session_id FROM auth_tokens WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return results

    @staticmethod
    def all():
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT token FROM user_tokens'
                cursor.execute(sql)
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return results

    @staticmethod
    def all_auth_token():
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT token FROM auth_tokens'
                cursor.execute(sql)
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return results

    @staticmethod
    def check(token):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_tokens WHERE token = %s'
                cursor.execute(sql, (token,))
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        if len(results) > 0 and results[0]['token'] == token:
            return results[0]['user_id']
        else:
            return False

    @staticmethod
    def delete(user_id, reset_case):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'DELETE FROM user_tokens WHERE user_id = %s AND reset_case = %s'
                cursor.execute(sql, (user_id, reset_case))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
