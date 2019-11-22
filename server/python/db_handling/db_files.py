import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBfiles:

    @staticmethod
    def db_insert_user_file(file_id, user_id, file_name, path, is_encrypted):
        db = DBconnector.create_db_connection()
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
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT id, file_name, file_description, path, is_encrypted FROM user_data WHERE user_id = %s'
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
        db = DBconnector.create_db_connection()
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
        db = DBconnector.create_db_connection()
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
        db = DBconnector.create_db_connection()
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
