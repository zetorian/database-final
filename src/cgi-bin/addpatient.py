#!/usr/bin/python

import mysql.connector
import sys
import random
import cgi,cgitb

cnx = mysql.connector.connect(user='root',password='newpassword',host='localhost')
cursor = cnx.cursor(buffered=True)

args = ""
query="use EMR"
cursor.execute(query)

#query = "INSERT INTO Patient (SSN, FName, LName, Phone, Address, InsuaranceCo, PrimaryDoctor) VALUES (%s, %s, %s, %s, %s, %s, %s);"
#args = ""
#cursor.execute(query, args)

cgitb.enable() #for debugging
form = cgi.FieldStorage()

isPosted = form.getvalue('isposted')



fnameErrorMsg = ("Not a valid name")
lnameErrorMsg = ("Invalid Last Name")
SSNErrorMsg = ("Invalid SSN")
SSNTakenMsg = ("Patient already exists with that SSN")
phoneErrorMsg = ("Invalid phone number")
addrErrorMsg = ("Please enter a valid address")
insuranceErrorMsg = ("Not a valid insurance company")
docErrorMsg = ("Doctor not registered in this system")

isError = False

ssnTaken = False

insuranceExists = False



if isPosted:

    fname = form.getvalue('fname')
    lname = form.getvalue('lname')
    SSN = form.getvalue('ssn')
    phone = form.getvalue('phone')
    addr = form.getvalue('addr')
    insurance = form.getvalue('insurance')
    doc = form.getvalue('doc')

    drSSN = None

    if SSN is not None:
        
        query ="SELECT * FROM Patient WHERE SSN ='" + SSN + "';"
        #query = "SELECT name FROM hospital;"
        args = (SSN)
        cursor.execute(query)
        #records = cursor.fetchall()
    
    if cursor.rowcount != 0:
        ssnTaken = True
        isError = True

    if doc is not None:
        docSplit = doc.split()
        if len(docSplit) != 2:
            drSSN = None
        else:
            doctorFirst = docSplit[0]
            doctorLast = docSplit[1]
            doctorFirst.lower()
            doctorLast.lower()
            query ="SELECT SSN FROM Doctor WHERE fname ='" + doctorFirst + "' AND lname = '" + doctorLast + "';"
            cursor.execute(query)

            if cursor.rowcount == 0:
                drSSN = None
            else:
                doctorReturn = cursor.fetchone()
                drSSN = doctorReturn[0]

    #testing to see if insurance company exists
    if insurance is not None:
        query ="SELECT * FROM insuranceCo WHERE name ='"+ insurance + "';"
        cursor.execute(query)
        if cursor.rowcount == 0:
            insuranceExists = False
            isError = True
        else:
            insuranceExists = True



    
    if drSSN is None or fname is None or lname is None or SSN is None or phone is None or addr is None or insurance is None or doc is None:
        isError = True
    
    if isError:
       
        #SSN = "100000030"
        print ("Content-type:text/html\r\n\r\n")
        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print("""<style> p.error {color: red;} </style>""")
        print ('</head>')
        print ('<body>')
        print ('<h2>Add Patient</h2>')

        #print("Rows: " + str(cursor.rowcount) + "<br>") #get rid of this later
        #print("SSN: " + SSN + "<br>")
        #print("Query: " + query + "<br>")
        #print("Args: " + args + "<br>")
        if drSSN is not None:
            print("Doctor: " + str(drSSN) + "<br>")

        print('<h3>')
        print("Name of the user is: %s" % fname)
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
        if lname:
            print('<input type="text" name="lname" value="%s"></input>' % lname)
        else:
            print('<input type="text" name="lname"></input>')
        print('</td>')
        print('<td>')
        if lname is None:
            print('<p class="error">')
            print(lnameErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>')
        print('Social Security Number')
        print('</td>')
        print('<td>')
        if SSN:
            print('<input type="text" name="ssn" value="%s"></input>' % SSN)
        else:
            print('<input type="text" name="ssn"></input>')
        print('</td>')
        print('<td>')
        if SSN is None:
            print('<p class="error">')
            print(SSNErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>')
        print('Phone Number')
        print('</td>')
        print('<td>')
        if phone:
            print('<input type="text" name="phone" value="%s"></input>' % phone)
        else:
            print('<input type="text" name="phone"></input>')
        print('</td>')
        print('<td>')
        if phone is None:
            print('<p class="error">')
            print(phoneErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>')
        print('Street Address')
        print('</td>')
        print('<td>')
        if addr:
            print('<input type="text" name="addr" value="%s"></input>' % addr)
        else:
            print('<input type="text" name="addr"></input>')
        print('</td>')
        print('<td>')
        if addr is None:
            print('<p class="error">')
            print(addrErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>')
        print('Insurance Company')
        print('</td>')
        #look up and cast to int
        print('<td>')
        if insurance:
            print('<input type="text" name="insurance" value="%s"></input>' % insurance)
        else:
            print('<input type="text" name="insurance"></input>')
        print('</td>')
        print('<td>')
        if insurance is None or not insuranceExists:
            print('<p class="error">')
            print(insuranceErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')

        print('<tr>')
        print('<td>')
        print('Primary Doctor')
        print('</td>')
        #look up and cast to social
        print('<td>')
        if doc:
            print('<input type="text" name="doc" value="%s"></input>' % doc)
        else:
            print('<input type="text" name="doc"></input>')
        print('</td>')
        print('<td>')
        if doc is None or drSSN is None:
            print('<p class="error">')
            print(docErrorMsg)
            print('</p>')
        print('</td>')
        print('</tr>')


        print('</table>')
        print('<br>')
        print('<input type="hidden" name="isposted" value="true"></input>')
        print('<input type="submit" value="Submit"></input>')
        print('</form>')
        if ssnTaken:
            print('<br>SSN taken<br>')
        else:
            print('<br>SSN not taken<br>')

        if insuranceExists:
            print('<br>Insurance Company Exists<br>')
        else:
            print('<br>Insurance Company Does Not Exist<br>')
        print ('</body>')
        print ('</html>')
    else:   #Here we store the results and tell the user we accepted the input
        query = "INSERT INTO patient (ssn, fname, lname, phone, address, insuranceCo, PrimaryDoctor) VALUES ('" + SSN + "', '" + fname + "', '" + lname + "', '" + phone + "','" + addr + "','" + insurance + "', '" + drSSN + "');"
        #addr is None or insurance is None or doc is None:
        cursor.execute(query)

        print ("Content-type:text/html\r\n\r\n")
        print ('<html>')
        print ('<head>')
        print ('<title>EMR System</title>')
        print("""<style> p.error {color: red;} </style>""")
        print ('</head>')
        print ('<body>')

        print ('<h2>Patient Added</h2>')

        print ('<br> <br>')
        print ('<form action="runme.py">')
        print ('<input type="submit" value="Return to Menu" />')
        print ('</form>')
        
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
    print('<input type="text" name="ssn"></input>')
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

cnx.commit()
cursor.close()
cnx.close()