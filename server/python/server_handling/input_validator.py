import cherrypy


class InputValidator:

    @staticmethod
    def check_session_value(value):
        if cherrypy.session.get(value):
            return cherrypy.session.get(value)
        else:
            return False

    @staticmethod
    def email_validator(email):
        if len(email) <= 50:
            return email if '@' in email else False
        else:
            return False

    @staticmethod
    def int_validator(var):
        if type(var) == int:
            return True
        else:
            return False

    @staticmethod
    def file_validator(file):
        print(type(file))
        if file.filename:
            return True
        else:
            return False
