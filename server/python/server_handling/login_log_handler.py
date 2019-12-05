import time
from datetime import datetime

from server.python.comm_handling.email_sender import EmailSender
from server.python.db_handling.db_logs import DBlogs


class LLogHandler:

    # Funktion zur Überprüfung der Login Versuche
    @staticmethod
    def check_login_logs(user_id):
        log = DBlogs.get_login_log(user_id)
        if len(log) < 1:
            DBlogs.insert(user_id)
            log = DBlogs.get_login_log(user_id)
        return LLogHandler.check_timestamp(user_id, log)

    # Funktion zur Überprüfung des letzten Login Versuchs
    @staticmethod
    def check_timestamp(user_id, log):
        current_timestamp = int(time.time())
        log_timestamp = log[0]['timestamp']
        login_time = current_timestamp - log_timestamp
        if login_time > 60:
            DBlogs.delete_login_log(user_id)
            DBlogs.insert(user_id)
            return DBlogs.get_login_log(user_id)
        else:
            return log

    # Funktion zum Zählen der Login Versuche
    @staticmethod
    def count_tries(user_id, log, email):
        counter = log[0]['counter']
        if counter > 5:
            warning_date = datetime.fromtimestamp(log[0]['timestamp'])
            warning_message = 'Warning: We registered an anomaly for you account login. Time: %s' % warning_date
            warning_subject = 'Warning: Anomaly registered'
            EmailSender.send_mail(warning_message, warning_subject, email)
            return False
        else:
            counter += 1
            DBlogs.update_login_log(user_id, counter)
            return True
