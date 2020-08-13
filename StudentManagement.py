import cherrypy
import sqlite3
from time import sleep

databaseName = "Database/students.db"


class StudentManagement(object):

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
                            <li><a href="index">Homepage</a></li>
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                            <li><a href="update">Update Student Info.</a></li>
                            <li><a href="department">Departments</a></li>
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

    @cherrypy.expose
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
                        <td align="center">""" + str(row[0]) + """</td>
                        <td align="center">""" + str(row[2]) + """</td>
                        <td align="center">""" + str(row[3]) + """</td>
                        <td align="center">""" + str(row[4]) + """</td>
                        <td align="center">""" + str(row[5]) + """</td>
                    </tr>
                </tbody>
            """
            table += rowData
        # Closing connection and wrapping up html with our return line
        conn.close()
        return table + "</table></div></body></html>"

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
                            <li><a href="index">Homepage</a></li>
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                            <li><a href="update">Update Student Info.</a></li>
                            <li><a href="department">Departments</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                        </ul>
                    </div>
                </nav>
                <div style="width: 50%; float:left">

                <div class="margin">
                <h3><b>Enter Student Details</b></h3>
                <br>
                    <form method="post" action="createStudent">""" + optionalString + """
                    <div class="form-row">
                        <div class="form-group ">
                            <label>First Name:</label>
                            <input type="text" class="form-control" placeholder="First name" name="fname" required>
                        </div>
                        <div class="form-group ">
                            <label>Last Name:</label>
                            <input type="text" class="form-control" placeholder="Last name" name="lname" required>
                        </div>
                        <div class="form-group">
                            <label>Roll. No</label>
                            <input type="text" class="form-control" placeholder="Roll No." name="rollno" required>
                        </div>
                        <div class="form-group">
                            <label>GPA</label>
                            <input type="text" class="form-control" placeholder="GPA" name="gpa" required>
                        </div>
                        <div class="form-group">
                            <label>Credit Hours</label>
                            <input type="text" class="form-control" placeholder="Credit Hours" name="creditHours" required>
                        </div>
                        <div>
                        <label>Gender</label><br>
                            <input type="radio" id="Male" name="gender" value="Male">
                            <label for="male">Male</label><br>
                            <input type="radio" id="Female" name="gender" value="Female">
                            <label for="female">Female</label><br>
                            <input type="radio" id="Other" name="gender" value="Other">
                            <label for="other">Other</label>
                        <div>
                        <div class="form-group">
                            <label>Mobile No.</label>
                            <input type="text" class="form-control" placeholder="Enter Mobile Number" name="phone" required>
                        </div>
                        
                    </div>
                        <button type="submit" value="Submit" class="btn btn-primary" style="float: right;">Submit</button>
                        <br>
                        <br><br><br>
                    </form>
                </div>
                </div>
            </body>
        </html>
        """

    @cherrypy.expose
    def createStudent(self, rollno, fname, lname, gpa, creditHours, gender, phone):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT RollNo from Students"):
            # If a student already has the new ID, we make them try again
            if int(row[0]) == int(rollno):
                print("Invalid ID!")
                return self.new(errorValue="A student with ID #" + str(rollno) + " already exists.")
        # If we have a unique ID, then we add the student to the database via SQL and return to the front page
        name = " ".join([fname, lname])
        c.execute("INSERT INTO Students VALUES ('"
                  + str(name) + "','"
                  + str(rollno) + "','"
                  + str(gpa) + "','"
                  + str(creditHours) + "','"
                  + str(gender) + "','"
                  + str(phone) + "')"
                  )
        conn.commit()
        conn.close()

        return self.index()

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
                            <li><a href="index">Homepage</a></li>
                            <li><a href="new">Create Student</a></li>
                            <li><a href="delete">Remove Student</a></li>
                            <li><a href="update">Update Student Info.</a></li>
                            <li><a href="department">Departments</a></li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                        </ul>
                    </div>
                </nav>
                <body>
                
            <div style="width: 40%; float:left">
                <div class="margin">
                <form method="post" action="removeStudent">""" + optionalString + """
                    <h3><b>Deleting a Student from the System...</b></h3>
                    <br>
                    Enter the Roll Number of the student you want to delete : <br><br>
                    <input type="text" class="form-control" placeholder="Enter Roll. No." name="rollno" required>
                    <br>
                    <button type="submit" value="Submit">Delete</button>
                </form>
                </div>
            </div>
        </body></html>"""

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

    @cherrypy.expose
    def update(self, errorValue=""):
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
                <nav class="navbar navbar-inverse">
                        <div class="container-fluid">
                            <div class="navbar-header">
                              <a class="navbar-brand" href="#"><b>Student Management System</b></a>
                            </div>
                            <ul class="nav navbar-nav">
                                <li><a href="index">Homepage</a></li>
                                <li><a href="new">Create Student</a></li>
                                <li><a href="delete">Remove Student</a></li>
                                <li><a href="update">Update Student Info.</a></li>
                                <li><a href="department">Departments</a></li>
                            </ul>
                            <ul class="nav navbar-nav navbar-right">
                                <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                            </ul>
                        </div>
                    </nav>
                    <body>

                <div style="width: 30%; float:left">
                    <div class="margin">
                     <form method="post" action="search">""" + optionalString + """
                        <h3><b>Student Info. Update</b></h3>
                          <div class="input-group">
                            <input type="text" class="form-control" placeholder="Enter Roll. No." name="rollno" required>
                            <div class="input-group-btn">
                              <button class="btn btn-default" type="submit">
                                <i class="glyphicon glyphicon-search"></i>
                              </button>
                            </div>
                          </div>
                    </form>
                    """ + self.generateStudentUpdateTable() + """

                    </div>
                </div>
            </body></html>"""

    @cherrypy.expose
    def generateStudentUpdateTable(self, param, input):
        if param == "update":
            sleep(0.05)
            with sqlite3.connect(databaseName) as c:
                r = c.execute("SELECT * FROM benutzer")
                response = "<table width='100%' class='table table-striped table-bordered'" \
                           "cellspacing='0'><tr><td>Nr</td><td>Firstname</td><td>Lastname</td><td>Address</td><td>Qualification</td>" \
                           "<td>Email</td><td>Edit</td></tr>"
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + \
                                row[3] + "</td><td>" + row[4] + "</td><td>" \
                                + row[5] + "</td><td> <button onClick='updateBenutzer(" + str(row[0]) + ")'>Edit" \
                                                                                                        "</button></td></tr>"
                response += '</table>'
            return response

        if param == "getBenutzer":
            with sqlite3.connect(databaseName) as c:
                r = c.execute("SELECT * FROM benutzer WHERE nr=" + input)
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response = str(row[0]) + "#" + row[1] + "#" + row[2] + "#" + row[3] + "#" + row[4] + "#" + row[
                        5] + "#" + row[6];
            return response

        if param == "updateBenutzer":
            with sqlite3.connect(databaseName) as c:
                liste = input.split('#')
                c.execute("UPDATE benutzer SET firstname='" + liste[1] + "',lastname='"
                          + liste[2] + "',address='" + liste[3] + "',qualification='" + liste[4] + "',email='" + liste[
                              5] + "',password='" + liste[6] + "' WHERE nr=" + liste[0])
                return "Inserted successful."

        return "Ungültige Anfrage"

    @cherrypy.expose
    def department(self):
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
                                    <li><a href="index">Homepage</a></li>
                                    <li><a href="new">Create Student</a></li>
                                    <li><a href="delete">Remove Student</a></li>
                                    <li><a href="update">Update Student Info.</a></li>
                                    <li><a href="department">Departments</a></li>
                                </ul>
                                <ul class="nav navbar-nav navbar-right">
                                    <li><a href="login"><span class="glyphicon glyphicon-user"></span> Log Out</a></li>
                                </ul>
                            </div>
                        </nav>
                        <br>
                        """ + self.generateDeptTable() + """
                    </body>
                </html>"""

    @cherrypy.expose
    def generateDeptTable(self):
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

                                    <th align="center">Roll No</th>
                                    <th align="center">Name</th>
                                    <th align="center">CN</th>


                                </tr>
                            </thead>
                """
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        query = """SELECT RollNo, Name, CourseName from Students s, Course c where c.CourseId=s.CourseId"""
        c.execute(query)
        result = c.fetchall()
        for row in result:
            rowData = """
                        <tbody>
                            <tr>

                                <td align="center">""" + str(row[0]) + """</td>
                                <td align="center">""" + str(row[1]) + """</td>
                                <td align="center">""" + str(row[2]) + """</td>
                                

                            </tr>
                        </tbody>
                    """
            table += rowData
        # Closing connection and wrapping up html with our return line
        conn.close()
        return table + "</table></div></body></html>"


if __name__ == '__main__':
    cherrypy.quickstart(StudentManagement(), '/')
