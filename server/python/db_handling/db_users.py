import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector
from server.python.db_handling.hash_handler import HashHandler


class DBusers:

    @staticmethod
    def db_get_users():
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM users'
                cursor.execute(sql)
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return results

    @staticmethod
    def db_check_user(email, password):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT id, email, password FROM users WHERE email = %s'
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

    @staticmethod
    def db_get_user_settings(user_id):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT t2.description, setting_value FROM user_setting as t1 JOIN settings as t2 ON ' \
                      't1.settings_id = t2.id WHERE t1.user_id = %s '
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
                settings = {}
                for entry in result:
                    settings[entry['description']] = int(entry['setting_value'])

        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return settings

    @staticmethod
    def db_insert_user(email, password):
        db = DBconnector.create_db_connection()
        hashed_password = HashHandler.hash_password(password)
        try:
            with db.cursor() as cursor:
                sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
                cursor.execute(sql, (email, hashed_password))
                db.commit()
                sql = 'SELECT id FROM users WHERE email = %s'
                cursor.execute(sql, (email,))
                db.commit()
                result = cursor.fetchall()
                sql = 'INSERT INTO user_setting (user_id, settings_id, setting_value) VALUES (%s, 1, 1)'
                cursor.execute(sql, (result[0]['id'],))
                db.commit()
                sql = 'INSERT INTO user_setting (user_id, settings_id, setting_value) VALUES (%s, 2, 0)'
                cursor.execute(sql, (result[0]['id'],))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return result[0]['id']
