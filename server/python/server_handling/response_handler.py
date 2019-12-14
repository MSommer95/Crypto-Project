import cherrypy


class ResponseHandler:

    @staticmethod
    def unauthorized_response():
        cherrypy.lib.sessions.expire()
        cherrypy.response.status = 401
        return {'message': 'Access denied: Unauthorized'}

    @staticmethod
    def bad_request_response():
        cherrypy.response.status = 500
        return {'message': 'Your request was not correct'}

    @staticmethod
    def too_many_requests_response():
        cherrypy.response.status = 418
        return {'message': 'Too many tries.'}

    @staticmethod
    def forbidden_response():
        cherrypy.response.status = 403
        return {'message': 'Forbidden Request'}
