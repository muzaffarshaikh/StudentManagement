import cherrypy
import sqlite3
from time import sleep

databaseName = "Database/students.db"


class StudentManagement(object):

    @cherrypy.expose
    def login(self, errorValue=""):
        optionalString = ""
        if errorValue != "":
            optionalString = """<font color="red">""" + errorValue + """</font><br>"""
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
            <h2 align="center"><b>Student Management System</b></h2>   
                <div class="login-form">    

                    <form method="post" action="/auth/login">
                    <h3 align="center"><b>LOG IN<b></h3>
                        <input type="hidden" name="from_page" value="%(from_page)s" /><br/>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Username" required="required" name="username" /><br />
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="Password" required="required" name="password" /><br />
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary btn-block" type="submit">Log In</button>
                        </div>
                    </form>
                 </div>
                    
            </body>
        </html>"""

    @cherrypy.expose
    def userLogin(self, username, password):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        query = conn.execute("select Username from Users")

        for row in query:
            if username in row:
                print("%s" % username)
                pas = conn.execute("SELECT Password FROM Users WHERE Username = %s" % username)

                if password in pas:
                    return self.index()
                else:
                    return self.login(errorValue="Incorrect Password for" + username + ".")
                conn.close()
                return
        print
        "Incorrect ID! If you are not a user, please register here."

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
            <body style="background-color:#e6ded5;">
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
                <footer class="page-footer font-small blue">
                  <div class="footer-copyright text-center py-3">© 2020 Copyright:
                    <a href="http://localhost:8080"> smsystem.com </a>
                  </div>
                </footer>
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
            <body style="background-color:#e6ded5;">
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
        for row in c.execute("SELECT * from Students order by RollNo"):
            rowData = """
                <tbody>
                    <tr>
                        <td align="center">""" + str(row[2]) + """</td>
                        <td align="center">""" + str(row[0]) + """ """ + str(row[1]) + """</td>
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
            body {
              background-image: url('background.png');
            }
            </style>
            </head>
            <body style="background-color:#e6ded5;">
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
                        <br>
                        <div class="form-group">
                        <label>Course</label>
                             <select name="course" id="course" class="form-control">
                              <option disabled selected value> -- Select a Course -- </option>
                              <option value="1">MSc. I.T.</option>
                              <option value="2">BSc. CS</option>
                              <option value="3">BVoc.</option>
                              <option value="4">Literature</option>
                              <option value="5.">Communication Skills</option>
                              <option value="6">Drama</option>
                              <option value="7">Probability Statistics</option>
                              <option value="8">Data Analytics</option>
                              <option value="9">Calculus</option>
                              <option value="10">Oceonography</option>
                              <option value="11">Geomorphology</option>
                              <option value="12">Astro Physics</option>
                              <option value="13">Quantum Physics</option>
                            </select>
                        </div>
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
    def createStudent(self, rollno, fname, lname, gpa, creditHours, gender, phone, course):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT RollNo from Students"):
            # If a student already has the new ID, we make them try again
            if int(row[0]) == int(rollno):
                print("Invalid ID!")
                return self.new(errorValue="A student with ID #" + str(rollno) + " already exists.")
        # If we have a unique ID, then we add the student to the database via SQL and return to the front page
        c.execute("INSERT INTO Students VALUES ('"
                  + str(fname) + "','"
                  + str(lname) + "','"
                  + str(rollno) + "','"
                  + str(gpa) + "','"
                  + str(creditHours) + "','"
                  + str(gender) + "','"
                  + str(phone) + "','"
                  + str(course) + "')"
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
                <body style="background-color:#e6ded5;">
                
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
            optionalString = """<font color="black">""" + errorValue + """</font><br>"""

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
                  margin-left: 65px;
                  margin-right: 80px;
                  
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
                    <body style="background-color:#e6ded5;">

                <div style="width: 60%; float:left">
                    <div class="margin">
                     <form method="post" action="searchStudent">
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
                    """ + optionalString + """
                    </div>
                </div>
            </body></html>"""

    @cherrypy.expose
    def searchStudent(self, rollno):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT RollNo from Students"):
            if int(row[0]) == int(rollno):
                html = """
                        <html>
                            <head>
                              <title>Bootstrap Example</title>
                              <meta charset="utf-8">
                              <meta name="viewport" content="width=device-width, initial-scale=1">
                              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                              <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
                            </head>
                            <body style="background-color:#e6ded5;">
                        """
                for row in c.execute(
                        "select FirstName, LastName, RollNo, GPA, Credit, Gender, Phone, CourseName from Students s, Course c WHERE s.CourseId=c.CourseId and RollNo = " + str(
                                rollno)):
                    form = """
                                <div float:"right">
                                <form method="post" action="updateStudent">
                                    <div class="form-row">
                                        <div class="form-group ">
                                        <div class="form-group">
                                            <label>Roll. No</label>
                                            <input type="text" class="form-control" value=""" + str(row[2]) + """ name="rollno" required disabled>
                                        </div>
                                            <label>First Name:</label>
                                            <input type="text" class="form-control" value=""" + str(row[0]) + """ name="fname" required>
                                        </div>
                                        </div class="form-group">
                                            <label>Last Name:</label>
                                            <input type="text" class="form-control" value=""" + str(row[1]) + """ name="lname" required>
                                        </div>
                                        <div class="form-group">
                                            <label>GPA</label>
                                            <input type="text" class="form-control" value=""" + str(row[3]) + """ name="gpa" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Credit Hours</label>
                                            <input type="text" class="form-control" value=""" + str(row[4]) + """ name="creditHours" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Gender</label>
                                            <input type="text" class="form-control" value=""" + str(row[5]) + """ name="gender" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Mobile No.</label>
                                            <input type="text" class="form-control" value=""" + str(row[6]) + """ name="phone" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Course</label>
                                            <input type="text" class="form-control" value=""" + str(row[7]) + """ name="course" required disabled>
                                        </div>
                                        
                                        <button type="submit" value="Submit" class="btn btn-primary" style="float: right;">Update</button>
                                    </div>
                                        <br><br><br><br><br><br>
                                    </form>
                                </div>
                                </table>
                                </div>
                            """
                html += form
                conn.commit()
                conn.close()
                return self.update(html + "</body></html>")

            # If we never find a student with rollno, we reload the "delete" page with an error
        return self.update(errorValue="There is no student with an Roll Number #" + str(rollno) + ".")

    @cherrypy.expose
    def updateStudent(self, rollno, fname, lname, gpa, creditHours, gender, phone, course):
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        c.execute(
            "update Students set FirstName='" + fname + "', LastName='" + lname + "', GPA='" + gpa + "', Credit='" + creditHours + "', Gender='" + gender + "', Phone='" + phone + "', Course='" + course + " where RollNo='" + rollno)
        conn.commit()
        conn.close()

        return self.index

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
                    <body style="background-color:#e6ded5;">
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
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
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
                    <body style="background-color:#e6ded5;"> 
                    <div>
                    </div>
                        <div class="container">
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr class="info">

                                    <th align="center">Roll No</th>
                                    <th align="center">Name</th>
                                    <th align="center">Department</th>
                                    <th align="center">Course</th>
                                </tr>
                            </thead>
                """
        query = """SELECT RollNo, FirstName, LastName, DeptName, CourseName from Students s, Course c, Department d where c.CourseId=s.CourseId and d.DeptId=c.DeptId order by d.DeptName"""
        c.execute(query)
        result = c.fetchall()
        for row in result:
            rowData = """
                        <tbody>
                            <tr>
                                <td align="center">""" + str(row[0]) + """</td>
                                <td align="center">""" + str(row[1]) + """ """ + str(row[2]) + """</td>
                                <td align="center">""" + str(row[3]) + """</td>
                                <td align="center">""" + str(row[4]) + """</td>
                            </tr>
                        </tbody>
                    """
            table += rowData
        # Closing connection and wrapping up html with our return line
        conn.close()
        return table + "</table></div></body></html>"


if __name__ == '__main__':
    cherrypy.quickstart(StudentManagement(), '/')
