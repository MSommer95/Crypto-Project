import cherrypy


class ResponseHandler:

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
