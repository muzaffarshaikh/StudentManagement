import cherrypy
import sqlite3

databaseName = "Database/students.db"


class StudentManagement(object):

    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head>
            <title>Student Management System</title>
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
                  <a href="#"><i><b>Student<br>Management<br>System<b><i></a>
                  <a href="#"><form method="get" action="new"><button type="submit">Create new Student</button></form></a>
                  <a href="#"><form method="get" action="delete"><button type="submit">Delete a Student</button></form></a>
                  
                  
                  <a href="#" class="right">Link</a>
                </div>
                <br>
                """ + self.generateStudentTable() + """
                <br>
                <br>
                    <form method="get" action="new">
                      <button type="submit">Create new Student</button>
                    </form>
                    <form method="get" action="delete">
                      <button type="submit">Delete a Student</button>
                    </form>
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

        return """<html><body>
                    <h3>Student Addition</h3>
                    <form method="get" action="generateStudent">""" + optionalString + """
                        Name:<br>
                        <input type="text" value="" name="name" /><br>
                        Roll Number #:<br>
                        <input type="number" value="" min="0" step="1" name="rollno"/><br>
                        P.R. Number #:<br>
                        <input type="number" value="" min="0" step="1" name="pr"/><br>
                        GPA:<br>
                        <input type="text" value="" name="gpa"/><br>
                        Credit Hours:<br>
                        <input type="text" value="" name="creditHours"/><br><br>
                        Gender:<br>
                        <input type="text" value="" name="gender"/><br><br>
                        Phone:<br>
                        <input type="text" value="" name="phone"/><br><br>
                        <button type="submit" value="Submit">Submit</button>
                    </form>
                  </body>
                </html>"""

    # Displays a small dialog to decide which student to remove via ID value. Like the new() method,
    # this one has the optional parameter "errorValue" for displaying potential errors
    @cherrypy.expose
    def delete(self, errorValue=""):
        optionalString = ""
        if errorValue != "":
            optionalString = """<font color="red">""" + errorValue + """</font><br>"""

        return """<html><body>
            <form method="get" action="removeStudent">""" + optionalString + """
                <h3>Student Removal</h3>
                Enter the Roll Number # of the student you want removed:<br>
                <input type="text" value="" name="rollno"/><br><br>
                <button type="submit" value="Submit">Submit</button>
            </form>
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
                <table style="width:50%">
                <tr>
                    <th>Roll No.</th>
                    <th>P.R. Number</th>
                    <th>Name</th>
                    <th>GPA</th>
                    <th>Credit Hours</th>
                    <th>Gender</th>
                    <th>Phone</th>
                </tr>
        """
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        for row in c.execute("SELECT * from Students"):
            rowData = """<tr>
            <td align="center">""" + str(row[1]) + """</td>
            <td align="center">""" + str(row[2]) + """</td>
            <td align="center">""" + str(row[0]) + """</td>
            <td align="center">""" + str(row[3]) + """</td>
            <td align="center">""" + str(row[4]) + """</td>
            <td align="center">""" + str(row[5]) + """</td>
            <td align="center">""" + str(row[6]) + """</td></tr>"""
            table += rowData
        # Closing connection and wrapping up html with our return line
        conn.close()
        return table + "</table>"

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
