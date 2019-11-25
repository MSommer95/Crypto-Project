import logging

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBdevices:

    @staticmethod
    def get_devices_by_user_id(user_id):
        db = DBconnector.create_db_connection()
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
    def get_devices_by_device_id(device_id):
        db = DBconnector.create_db_connection()
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
    def get_active_devices_by_user_id(user_id):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_device WHERE user_id = %s AND device_is_active = 1'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result

    @staticmethod
    def insert_user_device(user_id, device_id, device_name):
        db = DBconnector.create_db_connection()
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
    def set_active_user_device(user_id, device_id, activate_value):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_device SET device_is_active = %s WHERE user_id = %s AND id = %s'
                cursor.execute(sql, (activate_value, user_id, device_id))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def deactivate_all_user_devices(user_id):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_device SET device_is_active = 0 WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def delete_device(device_id, user_id):
        db = DBconnector.create_db_connection()
        try:
            with db.cursor() as cursor:
                sql = 'DELETE FROM user_device WHERE id = %s AND user_id = %s'
                cursor.execute(sql, (device_id, user_id))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        return result
