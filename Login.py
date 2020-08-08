#!python
import cherrypy
from cherrypy._cpserver import Server

from AuthController import AuthController, require, member_of, name_is


class RestrictedArea:
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group

    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""


class Root:
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    restricted = RestrictedArea()

    @cherrypy.expose
    @require()
    def index(self):
        return """Welcome!"""


if __name__ == '__main__':
    cherrypy.quickstart(Root())
