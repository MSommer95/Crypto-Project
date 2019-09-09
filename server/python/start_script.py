
import cherrypy


class Index(object):

    @cherrypy.expose()
    def index(self):
        return open('../index.html')


if __name__ == '__main__':
    cherrypy.quickstart(Index())