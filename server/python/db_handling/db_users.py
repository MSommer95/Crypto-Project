import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector
from server.python.auth_handling.hash_handler import HashHandler


class DBusers:

    @staticmethod
    def get_user(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT email FROM users WHERE id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return results

    @staticmethod
    def get_user_id(email):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT id FROM users WHERE email = %s'
                cursor.execute(sql, (email,))
                db.commit()
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return results

    @staticmethod
    def check_user(email, password):
        db = DBconnector.connect()
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
    def get_user_settings(user_id):
        db = DBconnector.connect()
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
    def insert_user(email, password):
        db = DBconnector.connect()
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
                sql = 'INSERT INTO user_setting (user_id, settings_id, setting_value) VALUES (%s, 1, 0)'
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

    @staticmethod
    def update_email(user_id, email):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE users SET email = %s WHERE id = %s'
                cursor.execute(sql, (email, user_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
            return 'There was an error while updating the email-address \n'
        else:
            return 'Successfully updated email \n'
        finally:
            db.close()

    @staticmethod
    def update_password(user_id, password):
        db = DBconnector.connect()
        hashed_password = HashHandler.hash_password(password)
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE users SET password = %s WHERE id = %s'
                cursor.execute(sql, (hashed_password, user_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
            return 'There was an error while updating the password'
        else:
            return 'Successfully updated password'
        finally:
            db.close()

    @staticmethod
    def set_second_factor_option(user_id, settings_id, setting_value):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_setting SET setting_value = %s WHERE user_id = %s AND settings_id = %s'
                cursor.execute(sql, (setting_value, user_id, settings_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
