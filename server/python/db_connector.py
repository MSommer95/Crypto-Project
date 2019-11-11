import logging
import time

import pymysql.cursors

from server.python.hash_handler import HashHandler


# noinspection SqlNoDataSourceInspection
class DbConnector:

    @staticmethod
    def create_db_connection():
        params = {'dbname': 'project',
                  'user': 'root',
                  'password': 'HMpXB44P',  # root
                  'dbhost': '127.0.0.1',
                  'charset': 'utf8mb4'}

        db = pymysql.connect(host=params['dbhost'],
                             user=params['user'],
                             password=params['password'],
                             db=params['dbname'],
                             charset=params['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
        return db

    @staticmethod
    def db_get_users():
        db = DbConnector.create_db_connection()
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
        db = DbConnector.create_db_connection()
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
        db = DbConnector.create_db_connection()
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
    def db_check_for_used_otp(user_id, hotp):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_otp_used WHERE user_id = %s AND used_otp = %s'
                cursor.execute(sql, (user_id, hotp))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        if len(result) > 0:
            return True
        else:
            return False

    @staticmethod
    def db_insert_user_2fa(user_id, hotp):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                ts = int(time.time())
                sql = 'DELETE FROM user_otp WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                sql = 'INSERT INTO user_otp (user_id, current_otp, timestamp) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, hotp, ts))
                sql = 'INSERT INTO user_otp_used (user_id, used_otp, timestamp) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, hotp, ts))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def db_insert_user(email, password):
        db = DbConnector.create_db_connection()
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

    @staticmethod
    def db_check_2fa(user_id, hotp):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT current_otp, timestamp FROM user_otp WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        ts = int(time.time())
        db_hotp = result[0]['current_otp']
        db_time = result[0]['timestamp']

        past_time = ts - db_time

        if db_hotp == hotp and past_time < 60:
            return True
        else:
            return False

    @staticmethod
    def db_get_user_devices_by_user_id(user_id):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_device WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def db_get_user_devices_by_device_id(device_id):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_device WHERE device_id = %s'
                cursor.execute(sql, (device_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def db_insert_user_devices(user_id, device_id, device_name):
        db = DbConnector.create_db_connection()
        db_connection_state = 'pending'
        try:
            with db.cursor() as cursor:
                sql = 'INSERT INTO user_device (user_id, device_id, device_name) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, device_id, device_name))
                db.commit()
                db_connection_state = 'success'
        except pymysql.MySQLError as e:
            logging.error(e)
            db_connection_state = 'failed'
        finally:
            db.close()
            return db_connection_state

    @staticmethod
    def db_insert_user_file(file_id, user_id, file_name, path, is_encrypted):
        db = DbConnector.create_db_connection()
        db_connection_state = 'pending'
        try:
            with db.cursor() as cursor:
                sql = 'INSERT INTO user_data (id, user_id, file_name, path, is_encrypted) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql, (file_id, user_id, file_name, path, is_encrypted))
                db.commit()
                db_connection_state = 'success'
        except pymysql.MySQLError as e:
            logging.error(e)
            db_connection_state = 'failed'
        finally:
            db.close()
            return db_connection_state

    @staticmethod
    def db_get_user_files(user_id):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT id, file_name, path, is_encrypted FROM user_data WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def db_insert_file_key(user_id, file_id, key_path):
        db = DbConnector.create_db_connection()
        db_connection_state = 'pending'
        try:
            with db.cursor() as cursor:
                sql = 'INSERT INTO user_key (user_id, file_id, key_path) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, file_id, key_path))
                db.commit()
                db_connection_state = 'success'
        except pymysql.MySQLError as e:
            logging.error(e)
            db_connection_state = 'failed'
        finally:
            db.close()
            return db_connection_state

    @staticmethod
    def db_get_file_key(key_id, user_id):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_key WHERE file_id = %s AND user_id = %s'
                cursor.execute(sql, (key_id, user_id))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def db_get_user_file(file_id, user_id):
        db = DbConnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_data WHERE id = %s AND user_id = %s'
                cursor.execute(sql, (file_id, user_id))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result
