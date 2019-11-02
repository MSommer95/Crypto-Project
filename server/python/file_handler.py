from server.python.db_connector import DbConnector
import time


class FileHandler:

    @staticmethod
    def write_file(user_id, file):
        file_id = int(round(time.time() * 1000))
        print(type(file))
        size = 0
        path = '../storage/users/%s/files/unencrypted/%s' % (user_id, file.filename)
        # Write the unencrypted file
        with open(path, 'wb') as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)

        is_encrypted = 0
        DbConnector.db_insert_user_file(file_id, user_id, file.filename, path, is_encrypted)
