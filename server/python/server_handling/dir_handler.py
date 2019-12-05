import os


class DirHandler:

    # make_dir Funktion erstellt ein Verzeichnis beim angegebenen Pfad
    @staticmethod
    def create_dir(path):
        try:
            os.mkdir(path)
        except OSError:
            print('Creating Dir %s failed' % path)
        else:
            print('Successfully created Dir %s' % path)

    # create_dirs Funktion nimmt die user_id entgegen und erstellt alle notwendigen Ordner für den User
    @staticmethod
    def create_user_dirs(user_id):
        path = '../storage/users/'
        sub_dirs = [
            '/keys',
            '/files',
            '/others']
        sub_dirs_files = [
            '/unencrypted',
            '/encrypted']
        try:
            os.mkdir(path + user_id)
        except OSError:
            print('Creating Dir %s failed' % path)
        else:
            print('Successfully created Dir %s' % path)
            for dirs in sub_dirs:
                DirHandler.create_dir(path + user_id + dirs)
            for dirs in sub_dirs_files:
                DirHandler.create_dir(path + user_id + '/files' + dirs)

    # check_for_dirs Funktion nimmt eine user_id und überprüft, ob die notwendigen Ordner existieren / wenn nicht werden
    # die fehlenden Ordner erstellt
    @staticmethod
    def check_user_dirs(user_id):
        base_path = '../storage/users/%s' % user_id
        paths = [
            '/files',
            '/keys',
            '/others'
        ]
        inner_paths = [
            '/unencrypted',
            '/encrypted'
        ]

        if os.path.isdir(base_path):
            if os.path.isdir(base_path + paths[0]):
                for path in inner_paths:
                    if not os.path.isdir(base_path + paths[0] + path):
                        DirHandler.create_dir(base_path + paths[0] + path)
            else:
                DirHandler.create_dir(base_path + paths[0])
                for dirs in inner_paths:
                    DirHandler.create_dir(base_path + paths[0] + dirs)

            for x in range(1, len(paths)):
                if not os.path.isdir(base_path + paths[x]):
                    DirHandler.create_dir(base_path + paths[x])
        else:
            DirHandler.create_user_dirs(user_id)

    @staticmethod
    def check_server_dirs():
        base_path = '../storage'
        server_path = './server_handling'

        sub_paths = [
            '/api_key',
            '/email_key',
            '/users',
            '/other',
            '/salt'
        ]
        log_path = '/logs'

        if not os.path.isdir(base_path):
            DirHandler.create_dir(base_path)
            for path in sub_paths:
                DirHandler.create_dir(base_path + path)
        else:
            for path in sub_paths:
                if not os.path.isdir(base_path + path):
                    DirHandler.create_dir(base_path + path)
        if not os.path.isdir(server_path + log_path):
            DirHandler.create_dir(server_path + log_path)
