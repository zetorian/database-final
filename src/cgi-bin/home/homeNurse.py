#!/usr/bin/python3

import os
import http.cookies
import mysql.connector
from cgilib import loginlib

print('content-type: text/html')

result = loginlib.verify_login()
user = ""
userType=''
userSSN='100000179'
if result is not None: #if we get a valid result, we are signed in
    (ssn, role, user) = result
    userType = role
    userSSN = ssn
    if role != 'nurse':
        print("Location: /cgi-bin/cookie_test.py")
else: # else bump back to login page
    print("Location: /login.html")

print("\n\n")

print('<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>')
print('<h1>')
print('You are logged in as ' + user)
print('</h1>\n')
print('<body>\n')

cnx = mysql.connector.connect(user='cs',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)

cursor.execute('USE EMR;')
query = 'select lname,fname,ssn from patient;'
cursor.execute(query)

#
# Displays the list of patients view detail and to update info for
#

print('<table><caption>Choose Patient</caption>')
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
    print('<td>'+ lname+ '</td>')
    print('<td>'+ fname+ '</td>')
    print('<td><a href="./viewPatient.py?ssn='+ssn+'">'+ ssn+ '</td>')
    print('</tr>')

print('</tbody>')
