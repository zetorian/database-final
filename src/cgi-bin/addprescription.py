#!/usr/bin/python

import mysql.connector
import sys
import random
import cgi,cgitb
import datetime
from cgilib import loginlib

print ("Content-type:text/html")

result = loginlib.verify_login()
user = ""
userType=''
userSSN=''
if result is not None: #if we get a valid result, we are signed in
    (ssn, role, user) = result
    userType = role
    userSSN = ssn
else: # else bump back to login page
    print("Location: /login.html")
    print("\n\n")
    sys.exit()

print("\n\n")

cnx = mysql.connector.connect(user='cs',password='',host='localhost')
cursor = cnx.cursor(buffered=True)

args = ""
query="use EMR"
cursor.execute(query)

#query = "INSERT INTO Patient (SSN, FName, LName, Phone, Address, InsuaranceCo, PrimaryDoctor) VALUES (%s, %s, %s, %s, %s, %s, %s);"
#args = ""
#cursor.execute(query, args)

cgitb.enable() #for debugging
form = cgi.FieldStorage()

isPosted = form.getvalue('isPosted')

drErrorMsg = ('No doctor available by that name')
patientErrorMsg = ('No patient available by that name')

dateErrorMessage = ("Not a valid date")

isError = False

drExists = False

patientExists = False

currentDate = datetime.datetime.today()
currentDateString = currentDate.strftime("%Y-%m-%d")

date30future = datetime.datetime.today() + datetime.timedelta(30)
date30futureString = date30future.strftime("%Y-%m-%d")

#isPosted = True #Comment this out in final version

if isPosted: #we have already done this
    patientFirst = form.getvalue('patientFirst')
    patientLast = form.getvalue('patientLast')
    patientSSN = None
    docFirst = form.getvalue('docFirst')
    docLast = form.getvalue('docLast')
    docSSN = None
    
    datePrescribed = form.getvalue('datePrescribed')
    dateExpires = form.getvalue('dateExpires')

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

    #check to be sure expiration date is not before prescription date

    if isError:
        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print("""<style> p.error {color: red;} </style>""")
        print ('</head>')
        print ('<body>')
        print ('<h2>Add Prescription</h2>')
        print('<form action="./addprescription.py" method="post">')
        print('<table>')

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
        print('<td><br/></td>')
        print('<td>')
        print('<br/>') #flesh this out before demo
        print('</td>')
        print('</tr>')

        

        print('<tr>')
        print('<td>Date Prescribed</td>')
        print('<td>')
        print('<input type="date" name="datePrescribed" value="'+ datePrescribed + '"min="' + datePrescribed + '">')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>Expiration Date</td>')
        print('<td>')
        print('<input type="date" name="dateExpires" value="' + dateExpires + '"min="' + dateExpires + '">')
        print('</td>')
        print('</tr>')

        print('</table>')

        print('<input type="hidden" value="True" name="isPosted">')
        print('<br>')
        print('<input type="submit" value="Submit"></input>')
        print('</form>')

        print('<br><br>')

        print ('<form action="/cgi-bin/cookie_test.py">')
        print ('<input type="submit" value="Return to Menu" />')
        print ('</form>')


        print ('</body>')
        print ('</html>')

    else:
        #patientSSN = "503" #remove after testing
        #docSSN = "100000010" #remove after testing
        #datePrescribed = "2016-08-23" #remove after testing
        #dateExpires = "2018-08-04" #remove after testing

        query = "INSERT INTO presciption (patient, doctor, date, expires) VALUES ('" + patientSSN + "', '" + docSSN + "', '" + datePrescribed + "', '" + dateExpires + "');"
        cursor.execute(query)

        #patient VARCHAR(9), doctor VARCHAR(9), date DATETIME, expires DATETIME,

        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print ('</head>')
        print ('<body>')
        print ('<h2>Prescription for ' + patientFirst + ' ' + patientLast + ' Added</h2>')
        print ('<br><br>')

        print ('<form action="/cgi-bin/cookie_test.py">')
        print ('<input type="submit" value="Return to Menu" />')
        print ('</form>')

        print ('</body>')
        print ('</html>')

  

else: #First time loading the display
    print ('<html>')
    print ('<head>')
    print ('<title>EMR System</title>')
    print ('</head>')
    print ('<body>')
    print ('<h2>Add Prescription</h2>')
    print('<form action="./addprescription.py" method="post">')
    print('<table>')

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
    print('<td><br/></td>')
    print('<td>')
    print('<br/>') #flesh this out before demo
    print('</td>')
    print('</tr>')

    

    print('<tr>')
    print('<td>Date Prescribed</td>')
    print('<td>')
    print('<input type="date" name="datePrescribed" value="'+ currentDateString + '"min="' + currentDateString + '">')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>Expiration Date</td>')
    print('<td>')
    print('<input type="date" name="dateExpires" value="' + date30futureString + '"min="' + date30futureString + '">')
    print('</td>')
    print('</tr>')

    print('</table>')

    print('<input type="hidden" value="True" name="isPosted">')
    print('<br>')
    print('<input type="submit" value="Submit"></input>')
    print('</form>')

    print('<br><br>')

    print ('<form action="/cgi-bin/cookie_test.py">')
    print ('<input type="submit" value="Return to Menu" />')
    print ('</form>')


    print ('</body>')
    print ('</html>')

cnx.commit()
cursor.close()
cnx.close()
