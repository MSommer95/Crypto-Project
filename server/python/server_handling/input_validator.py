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
        return email if '@' in email else False
