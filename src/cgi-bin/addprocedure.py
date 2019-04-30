#!/usr/bin/python

import mysql.connector
import sys
import random
import cgi,cgitb
import datetime

cnx = mysql.connector.connect(user='root',password='newpassword',host='localhost')
cursor = cnx.cursor(buffered=True)

args = ""
query="use EMR"
cursor.execute(query)

cgitb.enable() #for debugging
form = cgi.FieldStorage()

isPosted = form.getvalue('isPosted')

drErrorMsg = ('No doctor available by that name')
patientErrorMsg = ('No patient available by that name')

dateErrorMessage = ("Not a valid date")
billErrorMsg = ("Not a valid amount")
paidErrorMsg = ("Not a valid amount")
overpaidErrMsg = ("Amount paid cannot exceed amount due")
locationErrMsg = ("Location Invalid")

isError = False

drExists = False

patientExists = False

locationExists = False

paidExists = False
paidErr = False
billedExists = False
billedErr = False
overpaid = False

currentDate = datetime.datetime.today()
currentDateString = currentDate.strftime("%Y-%m-%dT%H:%M")

date30future = datetime.datetime.today() + datetime.timedelta(30)
date30futureString = date30future.strftime("%Y-%m-%d")

#isPosted = True #Comment this out in final version

#isPosted = True # remove after testing
if isPosted: #we have already done this
    patientFirst = form.getvalue('patientFirst')
    patientLast = form.getvalue('patientLast')
    patientSSN = None
    docFirst = form.getvalue('docFirst')
    docLast = form.getvalue('docLast')
    docSSN = None
    paid = form.getvalue('paid')
    billed = form.getvalue('billed')
    paidFloat = None
    billedFloat = None
    procedureName = form.getvalue('procedureName')
    results = form.getvalue('results')
    
    dateAndTime = form.getvalue('dateAndTime')

    location = form.getvalue('location')

    if patientFirst is not None and patientLast is not None:
        #query to retrieve patient SSN
        query ="SELECT SSN FROM patient WHERE fname ='" + patientFirst + "' AND lname = '" + patientLast + "';"
        cursor.execute(query)
        if cursor.rowcount == 0:
            isError = True
        else:
            patientReturn = cursor.fetchone()
            patientSSN = patientReturn[0]
            patientExists = True
    else:
        isError = True
        patientExists = False

    if docFirst is not None and docLast is not None:
        #query to retrieve doctor SSN
        query ="SELECT SSN FROM doctor WHERE fname ='" + docFirst + "' AND lname = '" + docLast + "';"
        cursor.execute(query)
        if cursor.rowcount == 0:
            isError = True
        else:
            doctorReturn = cursor.fetchone()
            docSSN = doctorReturn[0]
            drExists = True
    else:
        isError = True
        drExists = False

    if paid is not None:
        try:
            paidFloat = float(paid)
            paidExists = True
        except ValueError:
            paidExists = False
            isError = True

    if billed is not None:
        try:
            billedFloat = float(billed)
            billedExists = True
        except ValueError:
            billedExists = False
            isError = True

    if paidFloat < 0 or paidFloat > 9999999:
        paidErr = True
        isError = True

    if (billedFloat < 0 or billedFloat > 9999999):
        isError = True
        billedErr = True

    if paidFloat > billedFloat:
        isError = True
        overpaid = True

    if location:
        locationExists = True
    else:
        isError = True

    #check to be sure expiration date is not before prescription date

    #isError = False #remove after testing
    if isError:
        print ("Content-type:text/html\r\n\r\n")
        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print("""<style> p.error {color: red;} </style>""")
        print ('</head>')
        print ('<body>')
        print ('<h2>Add Procedure</h2>')
        print('<form action="./addprocedure.py" method="post">')
        print('<table>')

        print('<tr>')
        print('<td>Procedure Name</td>')
        print('<td>')
        if procedureName:
            print('<input type="text" name="procedureName" value="%s"></input>' % procedureName)
        else:
            print('<input type="text" name="procedureName"></input>')#flesh this out before demo
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Patient First Name</td>')
        print('<td>')
        if patientFirst:
            print('<input type="text" name="patientFirst" value="%s"></input>' % patientFirst)
        else:
            print('<input type="text" name="patientFirst"></input>')#flesh this out before demo
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Patient Last Name</td>')
        print('<td>')
        if patientLast:
            print('<input type="text" name="patientLast" value="%s"></input>' % patientLast)
        else:
            print('<input type="text" name="patientLast">') #flesh this out before demo
        print('</td>')
        print('<td>')
        if not patientExists:
            print('<p class="error">' + patientErrorMsg + '</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Doctor First Name</td>')
        print('<td>')
        if docFirst:
            print('<input type="text" name="docFirst" value="%s"></input>' % docFirst)
        else:
            print('<input type="text" name="docFirst">') #flesh this out before demo
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Doctor Last Name</td>')
        print('<td>')
        if docLast:
            print('<input type="text" name="docLast" value="%s"></input>' % docLast)
        else:
            print('<input type="text" name="docLast">') #flesh this out before demo
        print('</td>')
        print('<td>')
        if not drExists:
            print('<p class="error">')
            print(drErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Procedure Location</td>')
        print('<td>')
        if location:
            print('<input type="text" name="location" value="%s"></input>' % location)
        else:
            print('<input type="text" name="location">')
        print('</td>')
        print('<td>')
        if not locationExists:
            print('<p class="error">')
            print(locationErrMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Copay</td>')
        print('<td>')
        if paidExists:
            print('<input type="text" name="paid" value="%s"></input>' % paid)
        else:
            print('<input type="text" name="paid">') #flesh this out before demo
        print('</td>')
        print('<td>')
        if (not paidExists) or paidErr:
            print('<p class="error">')
            print(paidErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Billed</td>')
        print('<td>')
        if billedExists:
            print('<input type="text" name="billed" value="%s"></input>' % billed)
        else:
            print('<input type="text" name="billed">') #flesh this out before demo
        print('</td>')
        print('<td>')
        print('<p class="error">')
        if (not billedExists) or billedErr:
            print(billErrorMsg)
        if overpaid:
            print(overpaidErrMsg)
        print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Procedure Results</td>')
        print('<td>')
        if results:
            print('<input type="text" name="results" value="%s"></input>' % results)
        else:
            print('<input type="text" name="results"></input>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td><br/></td>')
        print('<td>')
        print('<br/>') #flesh this out before demo
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Procedure Date and Time</td>')
        print('<td>')
        print('<input type="datetime-local" name="dateAndTime" value="'+ dateAndTime + '"min="' + dateAndTime + '">')
        print('</td>')
        print('</tr>')

        print('</table>')

        print('<input type="hidden" value="True" name="isPosted">')
        print('<br>')
        print('<input type="submit" value="Submit"></input>')
        print('</form>')

        print('<br><br>')

        print ('<form action="home.py">')
        print ('<input type="submit" value="Return to Menu" />')
        print ('</form>')


        print ('</body>')
        print ('</html>')

    else:
        #patientSSN = "503" #remove after testing
        #docSSN = "100000010" #remove after testing
        #datePrescribed = "2016-08-23" #remove after testing
        #dateExpires = "2018-08-04" #remove after testing

        #date and time converted to string
        #convert html date and time to sql date and time
        #dateTimeString = dateAndTime.strftime("%Y-%m-%d %H:%M:%S")

        #print float to 7.2 places of precision to database
        paidString = "%.2f" % paidFloat
        billedString = "%.2f" % billedFloat

        #query = "INSERT INTO Appointment (dateTime, location, doctor, patient, paid, ammountBilled) VALUES ('" + dateAndTime + "', '" + location + "', '" + docSSN + "', '" + patientSSN + "', '" + paidString + "', '" + billedString + "');"

        query = "INSERT INTO procedures (procedureName, dateTime, doctor, patient, results, paid, amountBilled) VALUES ('" + procedureName + "', '" + dateAndTime + "', '" + docSSN + "', '" + patientSSN + "', '" + results + "', '" + paidString + "', '" + billedString + "');"
        
        
        cursor.execute(query)

        #patient VARCHAR(9), doctor VARCHAR(9), date DATETIME, expires DATETIME,

        print ("Content-type:text/html\r\n\r\n")
        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print ('</head>')
        print ('<body>')
        print ('<h2>Procedure for ' + patientFirst + ' ' + patientLast + ' Added</h2>')
        print ('<br><br>')
        #print(paidString + "   " + billedString + "<br> <br>")
        print ('<form action="home.py">')
        print ('<input type="submit" value="Return to Menu" />')
        print ('</form>')

        print ('</body>')
        print ('</html>')

  

else: #First time loading the display
    print ("Content-type:text/html\r\n\r\n")
    print ('<html>')
    print ('<head>')
    print ('<title>EMR System</title>')
    print ('</head>')
    print ('<body>')
    print ('<h2>Add Procedure</h2>')
    print('<form action="./addprocedure.py" method="post">')
    print('<table>')

    print('<tr>')
    print('<td>Procedure Name</td>')
    print('<td>')
    print('<input type="text" name="procedureName">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Patient First Name</td>')
    print('<td>')
    print('<input type="text" name="patientFirst">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Patient Last Name</td>')
    print('<td>')
    print('<input type="text" name="patientLast">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Doctor First Name</td>')
    print('<td>')
    print('<input type="text" name="docFirst">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Doctor Last Name</td>')
    print('<td>')
    print('<input type="text" name="docLast">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Procedure Location</td>')
    print('<td>')
    print('<input type="text" name="location">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Copay</td>')
    print('<td>')
    print('<input type="text" name="paid">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Billed</td>')
    print('<td>')
    print('<input type="text" name="billed">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Procedure Results</td>')
    print('<td>')
    print('<input type="text" name="results">') #flesh this out before demo
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td><br/></td>')
    print('<td>')
    print('<br/>')
    print('</td>')
    print('</tr>')

    

    print('<tr>')
    print('<td>Procedure Date and Time</td>')
    print('<td>')
    print('<input type="datetime-local" name="dateAndTime" value="'+ currentDateString + '"min="' + currentDateString + '">')
    print('</td>')
    print('</tr>')

    print('</table>')

    print('<input type="hidden" value="True" name="isPosted">')
    print('<br>')
    print('<input type="submit" value="Submit"></input>')
    print('</form>')

    print('<br><br>')

    print ('<form action="home.py">')
    print ('<input type="submit" value="Return to Menu" />')
    print ('</form>')


    print ('</body>')
    print ('</html>')

cnx.commit()
cursor.close()
cnx.close()
