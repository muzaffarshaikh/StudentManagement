import cherrypy


class HomePage:

    @cherrypy.expose
    def index(self):
        return '''
            <html lang="en">
            <head>
            <title>Page Title</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            * {
              box-sizing: border-box;
            }
            
            body {
              font-family: Arial, Helvetica, sans-serif;
              margin: 0;
            }
            
            .header {
              padding: 80px;
              text-align: center;
              background: #1abc9c;
              color: white;
            }
            
            .header h1 {
              font-size: 40px;
            }
            
            .navbar {
              overflow: hidden;
              background-color: #333;
              position: sticky;
              position: -webkit-sticky;
              top: 0;
            }
            
            .navbar a {
              float: left;
              display: block;
              color: white;
              text-align: center;
              padding: 14px 20px;
              text-decoration: none;
            }
            
            
            .navbar a.right {
              float: right;
            }
            
            .navbar a:hover {
              background-color: #ddd;
              color: black;
            }
            
            .navbar a.active {
              background-color: #666;
              color: white;
            }
            
            .row {  
              display: -ms-flexbox; /* IE10 */
              display: flex;
              -ms-flex-wrap: wrap; /* IE10 */
              flex-wrap: wrap;
            }
            
            .side {
              -ms-flex: 30%; /* IE10 */
              flex: 30%;
              background-color: #f1f1f1;
              padding: 20px;
            }
            
            .main {   
              -ms-flex: 70%; /* IE10 */
              flex: 70%;
              background-color: white;
              padding: 20px;
            }
            
            .fakeimg {
              background-color: #aaa;
              width: 100%;
              padding: 20px;
            }
            
            /* Footer */
            .footer {
              padding: 20px;
              text-align: center;
              background: #ddd;
            }
            
            @media screen and (max-width: 700px) {
              .row {   
                flex-direction: column;
              }
            }
            
            @media screen and (max-width: 400px) {
              .navbar a {
                float: none;
                width: 100%;
              }
            }
            </style>
            </head>
            <body>
            <div class="navbar">
              <a href="#" class="active">Home</a>
              <a href="#">Link</a>
              <a href="#">Link</a>
              <a href="#" class="right">Link</a>
            </div>
            
            <div class="header">
              <h1>My Website</h1>
              <p>A <b>responsive</b> website created by me.</p>
            </div>
            
            
            
            </body>
            </html>
        '''


if __name__ == '__main__':
    cherrypy.quickstart(HomePage())
