import os


class DirHandler:

    # make_dir Funktion erstellt ein Verzeichnis beim angegebenen Pfad
    @staticmethod
    def create_dir(path):
        try:
            os.mkdir(path)
        except OSError:
            print(f'Creating Dir {path} failed')
        else:
            print(f'Successfully created Dir {path}')

    # create_dirs Funktion nimmt die user_id entgegen und erstellt alle notwendigen Ordner für den User
    @staticmethod
    def create_user_dirs(base_path, sub_paths, inner_paths):
        DirHandler.create_dir(base_path)
        DirHandler.create_user_sub_dirs(base_path, sub_paths, inner_paths)

    @staticmethod
    def create_user_sub_dirs(base_path, sub_paths, inner_paths):
        for path in sub_paths:
            if not os.path.isdir(f'{base_path}{path}'):
                DirHandler.create_dir(f'{base_path}{path}')
        for path in inner_paths:
            if not os.path.isdir(f'{base_path}{sub_paths[0]}{path}'):
                DirHandler.create_dir(f'{base_path}{sub_paths[0]}{path}')

    # check_for_dirs Funktion nimmt eine user_id und überprüft, ob die notwendigen Ordner existieren / wenn nicht werden
    # die fehlenden Ordner erstellt
    @staticmethod
    def check_user_dirs(user_id):
        base_path = f'../storage/users/{user_id}'
        sub_paths = [
            '/files',
            '/keys',
            '/others'
        ]
        inner_paths = [
            '/unencrypted',
            '/encrypted'
        ]

        if os.path.isdir(base_path):
            DirHandler.create_user_sub_dirs(base_path, sub_paths, inner_paths)
        else:
            DirHandler.create_user_dirs(base_path, sub_paths, inner_paths)

    @staticmethod
    def create_server_dirs(base_path, sub_paths, server_path, log_path):
        DirHandler.create_dir(base_path)
        for path in sub_paths:
            DirHandler.create_dir(f'{base_path}{path}')
        if not os.path.isdir(f'{server_path}{log_path}'):
            DirHandler.create_dir(f'{server_path}{log_path}')

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
            DirHandler.create_server_dirs(base_path, sub_paths, server_path, log_path)
        else:
            for path in sub_paths:
                if not os.path.isdir(f'{base_path}{path}'):
                    DirHandler.create_dir(f'{base_path}{path}')
