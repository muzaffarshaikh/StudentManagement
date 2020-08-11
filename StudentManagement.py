import cherrypy
import sqlite3

from UserLogin import Root

databaseName = "Database/students.db"


class StudentManagement(object):

    @cherrypy.expose
    def login(self):
        return """
        <html lang="en">
            <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Student Management System - Login</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> 
            <style>
                .login-form {
                    width: 340px;
                    margin: 50px auto;
                }
                .login-form form {
                    margin-bottom: 15px;
                    background: #f7f7f7;
                    box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
                    padding: 30px;
                }
                .login-form h2 {
                    margin: 0 0 15px;
                }
                .form-control, .btn {
                    min-height: 38px;
                    border-radius: 2px;
                }
                .btn {        
                    font-size: 15px;
                    font-weight: bold;
                }
            </style>
            </head>
            <body>
            <div class="login-form" style="width: 50%; float:left">
            </div>
            <div style="width: 50%; float:right">
                <div class="login-form" >
                    <form action="/examples/actions/confirmation.php" method="post">
                        <h2 class="text-center">Log in</h2>       
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Username" required="required">
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="Password" required="required">
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary btn-block">Log in</button>
                        </div>        
                    </form>
                </div>
            </div>
            </body>
        </html>                                		
     """

    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head>
                <title>Student Management System</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            </head>
            <body>
                <nav class="navbar navbar-inverse">
                    <div class="container-fluid">
                        <div class="navbar-header">
                          <a class="navbar-brand" href="#"><b>Student Management System</b></a>
                        </div>
                        <ul class="nav navbar-nav">
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                        </ul>
                    </div>
                </nav>
                <br>
                """ + self.generateStudentTable() + """
            </body>
        </html>"""

    # Displays all necessary prompts to create a new student in the table. The optional parameter
    # "errorValue" is only used if this page has to be reloaded due to a pre-existing ID value being used
    @cherrypy.expose
    def new(self, errorValue=""):
        # Created optionalString so that the error only shows up in the case of an error
        optionalString = ""
        if errorValue != "":
            optionalString = """<font color="red">""" + errorValue + """</font><br>"""

        return """
        <html>
            <head>
            <title>Student Management System</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            <style>
            div.margin {
              margin-left: 50px;
            }
            </style>
            </head>
            <body>
            <nav class="navbar navbar-inverse">
                    <div class="container-fluid">
                        <div class="navbar-header">
                          <a class="navbar-brand" href="#"><b>Student Management System</b></a>
                        </div>
                        <ul class="nav navbar-nav">
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                        </ul>
                    </div>
                </nav>
                
                <div class="margin">
                <h3>Enter Student Details</h3>
                    <form method="get" action="generateStudent">""" + optionalString + """
                        Name:<br>
                        <input type="text" value="" name="name" required/><br><br>
                        Roll Number #:<br>
                        <input type="number" value="" min="0" step="1" name="rollno" required/><br><br>
                        P.R. Number #:<br>
                        <input type="number" value="" min="0" step="1" name="pr" required/><br><br>
                        GPA:<br>
                        <input type="text" value="" name="gpa" required/><br><br>
                        Credit Hours:<br>
                        <input type="text" value="" name="creditHours" required/><br><br>
                        <label for="cars">Gender:</label>
                            <select name="gender" id="gender" required>
                              <option value=""></option>
                              <option value="Male">Male</option>
                              <option value="Female">Female</option>
                              <option value="Others">Others</option>
                            </select><br><br>
                        Phone:<br>
                        <input type="text" value="" name="phone" required/><br><br>
                        <button type="submit" value="Submit">Submit</button>
                    </form>
                </div>
            </body>
        </html>
        """

    # Displays a small dialog to decide which student to remove via ID value. Like the new() method,
    # this one has the optional parameter "errorValue" for displaying potential errors
    @cherrypy.expose
    def delete(self, errorValue=""):
        optionalString = ""
        if errorValue != "":
            optionalString = """<font color="red">""" + errorValue + """</font><br>"""

        return """<html>
        
        <head>
            <title>Student Management System</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            <style>
            div.margin {
              margin-left: 50px;
            }
            </style>
            </head>
            <nav class="navbar navbar-inverse">
                    <div class="container-fluid">
                        <div class="navbar-header">
                          <a class="navbar-brand" href="#"><b>Student Management System</b></a>
                        </div>
                        <ul class="nav navbar-nav">
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                        </ul>
                    </div>
                </nav>
                <body>
            <div class="margin">
            
            <form method="get" action="removeStudent">""" + optionalString + """
                <h3>Student Removal</h3>
                Enter the Roll Number # of the student you want removed:<br>
                <input type="text" value="" name="rollno"/><br><br>
                <button type="submit" value="Submit">Submit</button>
            </form>
            </div>
        </body></html>"""

    # This method either adds a new student to the list and returns to the index() front page,
    # or it reloads the "new" page when pre-existing IDs are entered, this time with an error for the user
    @cherrypy.expose
    def generateStudent(self, rollno, pr, name, gpa, creditHours, gender, phone):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT RollNo from Students"):
            # If a student already has the new ID, we make them try again
            if int(row[0]) == int(rollno):
                print("Invalid ID!")
                return self.new(errorValue="A student with ID #" + str(rollno) + " already exists.")
        # If we have a unique ID, then we add the student to the database via SQL and return to the front page
        c.execute("INSERT INTO Students VALUES ('"
                  + str(name) + "','"
                  + str(rollno) + "','"
                  + str(pr) + "','"
                  + str(gpa) + "','"
                  + str(creditHours) + "','"
                  + str(gender) + "','"
                  + str(phone) + "')"
                  )
        conn.commit()
        conn.close()

        return self.index()

    # This method is called in our index() method to create
    # our table of students from our SQL database
    def generateStudentTable(self):
        table = """
        <html>
            <head>
              <title>Bootstrap Example</title>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
              <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            </head>
            <body>
                <div class="container">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr class="info">
                            <th align="center">Roll No.</th>
                            <th align="center">P.R. Number</th>
                            <th align="center">Name</th>
                            <th align="center">GPA</th>
                            <th align="center">Credit Hours</th>
                            <th align="center">Gender</th>
                            <th align="center">Phone</th>
                        </tr>
                    </thead>
        """
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT * from Students"):
            rowData = """
                <tbody>
                    <tr>
                        <td align="center">""" + str(row[1]) + """</td>
                        <td align="center">""" + str(row[2]) + """</td>
                        <td align="center">""" + str(row[0]) + """</td>
                        <td align="center">""" + str(row[3]) + """</td>
                        <td align="center">""" + str(row[4]) + """</td>
                        <td align="center">""" + str(row[5]) + """</td>
                        <td align="center">""" + str(row[6]) + """</td>
                    </tr>
                </tbody>
            """
            table += rowData
        # Closing connection and wrapping up html with our return line
        conn.close()
        return table + "</table></div></body></html>"

    # This method either removes a student from the database and returns to the front page,
    # or it reprompts the "delete" page with an error when an invalid ID is entered
    @cherrypy.expose
    def removeStudent(self, rollno):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT RollNo from Students"):
            # If we find the student with that ID, we remove them and head back to the front page
            if int(row[0]) == int(rollno):
                c.execute("DELETE FROM Students WHERE RollNo = " + str(rollno))
                conn.commit()
                conn.close()
                return self.index()
        # If we never find a student with rollno, we reload the "delete" page with an error
        return self.delete(errorValue="There is no student with an Roll Number #" + str(rollno) + ".")


if __name__ == '__main__':
    cherrypy.quickstart(StudentManagement(), '/')