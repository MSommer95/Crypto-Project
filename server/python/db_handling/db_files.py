import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBfiles:

    @staticmethod
    def insert(file_id, user_id, file_name, path, is_encrypted):
        db = DBconnector.connect()
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
    def get_files(user_id):
        db = DBconnector.connect()
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
    def get_file(file_id, user_id):
        db = DBconnector.connect()
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

    @staticmethod
    def update_file(user_id, file_id, file_name, file_description, path):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_data SET file_name = %s, file_description = %s, path = %s WHERE id = %s AND user_id = %s'
                cursor.execute(sql, (file_name, file_description, path, file_id, user_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def insert_file_key(user_id, file_id, key_path):
        db = DBconnector.connect()
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
    def delete_file(file_id, user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'DELETE FROM user_data WHERE id = %s AND user_id = %s'
                cursor.execute(sql, (file_id, user_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
            return 'Something went wrong'
        else:
            return 'Successful file deleted'
        finally:
            db.close()

    @staticmethod
    def get_file_key(file_id, user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_key WHERE file_id = %s AND user_id = %s'
                cursor.execute(sql, (file_id, user_id))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def update_file_key(key_id, user_id, file_id, key_path):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_key SET key_path = %s WHERE id = %s AND user_id = %s AND file_id = %s'
                cursor.execute(sql, (key_path, key_id, user_id, file_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
