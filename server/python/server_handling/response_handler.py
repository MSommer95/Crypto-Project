import cherrypy

from server.python.user_handling.settings_handler import SettingsHandler


class ResponseHandler:

    @staticmethod
    def prepare_index(user_id):
        user_settings = SettingsHandler.prepare_user_settings(user_id)
        return open('../public/dist/index.html').read().format(auth_token=cherrypy.session.get('auth_token'),
                                                               email=user_settings['email'],
                                                               sec_fa_status=user_settings['status'],
                                                               sec_fa_email=user_settings['2FA-Mail'],
                                                               sec_fa_app=user_settings['2FA-App'])

    @staticmethod
    def unauthorized_response(message):
        cherrypy.lib.sessions.expire()
        cherrypy.response.status = 401
        return {'message': message}

    @staticmethod
    def bad_request_response(message):
        cherrypy.response.status = 500
        return {'message': message}

    @staticmethod
    def too_many_requests_response(message):
        cherrypy.response.status = 418
        return {'message': message}

    @staticmethod
    def forbidden_response(message):
        cherrypy.response.status = 403
        return {'message': message}

    @staticmethod
    def success_response(message):
        cherrypy.response.status = 200
        return {'message': message}
