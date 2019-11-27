import logging
import time

import pymysql

from server.python.db_handling.db_connector import DBconnector


class DBotp:

    @staticmethod
    def insert(user_id, otp):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                ts = int(time.time())
                sql = 'DELETE FROM user_otp WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                sql = 'INSERT INTO user_otp (user_id, current_otp, timestamp, verified) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql, (user_id, otp, ts, 0))
                sql = 'INSERT INTO user_otp_used (user_id, used_otp, timestamp) VALUES (%s, %s, %s)'
                cursor.execute(sql, (user_id, otp, ts))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def check_used(user_id, otp):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT * FROM user_otp_used WHERE user_id = %s AND used_otp = %s'
                cursor.execute(sql, (user_id, otp))
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
    def check_current(user_id, hotp):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT current_otp, timestamp, verified FROM user_otp WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

        ts = int(time.time())
        db_otp = result[0]['current_otp']
        db_time = result[0]['timestamp']
        db_otp_verified = result[0]['verified']

        past_time = ts - db_time

        if db_otp == hotp and past_time < 60 and not db_otp_verified:
            return True
        else:
            return False

    @staticmethod
    def update_verification(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'UPDATE user_otp SET verified = 1 WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()

    @staticmethod
    def check_verification(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT verified FROM user_otp WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        db_otp_verified = result[0]['verified']
        return db_otp_verified

    @staticmethod
    def get_used(user_id):
        db = DBconnector.connect()
        try:
            with db.cursor() as cursor:
                sql = 'SELECT used_otp, timestamp FROM user_otp_used WHERE user_id = %s'
                cursor.execute(sql, (user_id,))
                db.commit()
                result = cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            db.close()
        return result
