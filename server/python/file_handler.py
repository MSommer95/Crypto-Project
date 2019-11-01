class FileHandler:

    @staticmethod
    def write_file(user_id, file):

        print(type(file))
        size = 0
        # Write the unencrypted file
        with open('../storage/users/%s/files/unencrypted/%s' % (user_id, file.filename), 'wb') as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)
