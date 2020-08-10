import cherrypy

from AuthController import AuthController

auth = AuthController


class Welcome:

    @cherrypy.expose
    def index(self):
        return auth.get_loginform(self, username)


if __name__ == '__main__':
    cherrypy.quickstart(Welcome())
