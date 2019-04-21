#!/usr/bin/python

import mysql.connector
import sys
import random
import cgi,cgitb

cnx = mysql.connector.connect(user='root',password='newpassword',host='localhost')
cursor = cnx.cursor(buffered=True)

query="use EMR"
cursor.execute(query)

#query = "INSERT INTO Patient (SSN, FName, LName, Phone, Address, InsuaranceCo, PrimaryDoctor) VALUES (%s, %s, %s, %s, %s, %s, %s);"
#args = ""
#cursor.execute(query, args)

cgitb.enable() #for debugging
form = cgi.FieldStorage()

isPosted = True
#form.getvalue('isposted')

fname = form.getvalue('fname')
lname = form.getvalue('lname')
SSN = form.getvalue('SSN')
phone = form.getvalue('phone')
addr = form.getvalue('addr')
insurance = form.getvalue('insurance')
doc = form.getvalue('doc')

isError = True

if isPosted:

    ssnTaken = False
    
    fnameErrorMsg = ("Not a valid name")
    lnameErrorMsg = ("Invalid Last Name")
    SSNErrorMsg = ("Invalid SSN")
    SSNTakenMsg = ("Patient already exists with that SSN")
    PhoneErrorMsg = ("Invalid phone number")
    addrErrorMsg = ("Please enter a valid address")
    insuranceErrorMsg = ("Not a valid insurance company")
    docErrorMsg = ("Doctor not registered in this system")

    
    print ("Content-type:text/html\r\n\r\n")
    print ('<html>')
    print ('<head>')
    print ('<title>EMR System/title>')
    #print("""<style> p.error {color: red;} </style>""")
    print ('</head>')
    print ('<body>')
    print ('<h2>Add Patient</h2>')

    print('<h3>')
    #print("Name of the patient is: %s" % fname)
    print('</h3>')

    print('<form action="./addpatient.py" method="post">')
    print('<br>')
    print('<table>')
    print('<tr>')
    print('<td>')
    print('Frist Name')
    print('</td>')
    print('<td>')
    if fname:
        print('<input type="text" name="fname" value="%s"></input>' % fname)
    else:
        print('<input type="text" name="fname"></input>')
    print('</td>')
    print('<td>')
    if fname is None:
        print('<p class="error">')
        print(fnameErrorMsg)
        print('</p>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Last Name')
    print('</td>')
    print('<td>')
    print('<input type="text" name="lname"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Social Security Number')
    print('</td>')

    print('</td>')
    print('<td>')
    print('<input type="text" name="SSN"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Phone Number')
    print('</td>')
    print('<td>')
    print('<input type="text" name="phone"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Street Address')
    print('</td>')
    print('<td>')
    print('<input type="text" name="addr"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Insurance Company')
    print('</td>')
    print('<td>')
    #look up and cast to int
    print('<input type="text" name="insurance"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Primary Doctor')
    print('</td>')
    print('<td>')
    #look up and cast as social security number
    print('<input type="text" name="doc"></input>')
    print('</td>')
    print('</tr>')


    print('</table>')
    print('<br>')
    print('<input type="hidden" name="isposted" value="true"></input>')
    print('<input type="submit" value="Submit"></input>')
    print('</form>')
    print ('</body>')
    print ('</html>')


else:
    print ("Content-type:text/html\r\n\r\n")
    print ('<html>')
    print ('<head>')
    print ('<title>EMR System</title>')
    print ('</head>')
    print ('<body>')
    print ('<h2>Add Patient</h2>')

    print('<h3>')
    #print("Name of the user is: %s" % fname)
    print('</h3>')

    print('<form action="./addpatient.py" method="post">')
    print('<br>')
    print('<table>')
    print('<tr>')
    print('<td>')
    print('Frist Name')
    print('</td>')
    print('<td>')
    print('<input type="text" name="fname"></input>')
    print('</td>')
    print('</tr>')
    print('<tr>')
    print('<td>')
    print('Last Name')
    print('</td>')
    print('<td>')
    print('<input type="text" name="lname"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Social Security Number')
    print('</td>')
    print('<td>')
    print('<input type="text" name="SSN"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Phone Number')
    print('</td>')
    print('<td>')
    print('<input type="text" name="phone"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Street Address')
    print('</td>')
    print('<td>')
    print('<input type="text" name="addr"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Insurance Company')
    print('</td>')
    print('<td>')
    #look up and cast to int
    print('<input type="text" name="insurance"></input>')
    print('</td>')
    print('</tr>')

    print('<tr>')
    print('<td>')
    print('Primary Doctor')
    print('</td>')
    print('<td>')
    #look up and cast as social security number
    print('<input type="text" name="doc"></input>')
    print('</td>')
    print('</tr>')


    print('</table>')
    print('<br>')
    print('<input type="hidden" name="isposted" value="true"></input>')
    print('<input type="submit" value="Submit"></input>')
    print('</form>')
    print ('</body>')
    print ('</html>')