#!/usr/bin/python3

import os
import http.cookies
import mysql.connector
from cgilib import loginlib

print('content-type: text/html')

result = loginlib.verify_login()
user = ""
userType='patient'
userSSN='100000179'
if result is not None: #if we get a valid result, we are signed in
    (ssn, role, user) = result
    userType = role
    userSSN = ssn
    if role != 'doctor':
        print("Location: /cgi-bin/cookie_test.py")
else: # else bump back to login page
    print("Location: /login.html")

print("\n\n")

print('<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>')
print('<h1>')
print(('You are logged in as ' + user))
print('</h1>\n')
print('<body>\n')

cnx = mysql.connector.connect(user='cs',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
#print 'attempting query'
cursor.execute('USE EMR;')
query = 'select lname,fname,ssn from patient where primaryDoctor='+userSSN+';'
cursor.execute(query)


#
# Table to display the doctor's patients
#

print('<table><caption>Your Patients</caption>')
print('<thead>')
print('<tr>')
print('<th>Last Name </th>')
print('<th>First Name </th>')
print('<th>SSN </th>')
print('</tr>')
print('</thead>')
print('<tbody>')

for lname,fname,ssn in cursor:
    print('<tr>')
    print(('<td>'+ lname+ '</td>'))
    print(('<td>'+ fname+ '</td>'))
    print(('<td><a href="./viewPatient.py?ssn='+ssn+'">'+ ssn+ '</td>'))
    print('</tr>')

print('</tbody>')

#
# Table to display the doctors appointments
#

print('<table><caption>Your Appointments</caption>')
print('<thead>')
print('<tr>')
print('<th>Last Name </th>')
print('<th>First Name </th>')
print('<th>SSN </th>')
print('<th>Date/Time </th>')
print('<th>Location </th>')
print('</tr>')
print('</thead>')
print('<tbody>')

print('<br />')
print('<br />')
query = 'select dateTime, location, patient from Appointment where doctor ='+userSSN+ ';'

for dateTime,location,patient in cursor:
    cursor2.execute('SELECT lname, fname from patient where ssn ='+patient+';');
    for lname, fname in cursor2:
        
        print('<tr>')
        print(('<td>'+ lname+ '</td>'))
        print(('<td>'+ fname+ '</td>'))
        print(('<td>'+ patient+ '</td>'))
        print(('<td>'+ dateTime+ '</td>'))
        print(('<td>'+ location+ '</td>'))
        print('</tr>')

print('</tbody>')

print('</body>')
