import cherrypy


class Welcome:

    @cherrypy.expose
    def index(self):
        return '''
            <html lang="en">
            <div>
            <h1>Student Management System</h1>
            </div>
            <input type="submit" value="Log In" />
            <input type="submit" value="Sign Up" />
            </html>
        '''


if __name__ == '__main__':
    cherrypy.quickstart(Welcome())
