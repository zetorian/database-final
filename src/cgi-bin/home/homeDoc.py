#!/usr/bin/python2

import os
import Cookie
import mysql.connector

print 'content-type: text/html\n'

#this is hard coded for a doctor that exists in my test data
user='Moreen.Acker'
#if we got here the user must be a doctor
userType='doctor'
userSSN='100000001'

print '<h1>'
print 'You are logged in as ' + user
print '</h1>\n'
print '<body>\n'

cnx = mysql.connector.connect(user='root',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
#print 'attempting query'
cursor.execute('USE EMR;')
query = 'select lname,fname,ssn from patient where primaryDoctor='+userSSN+';'
cursor.execute(query)

print '<table><caption>Your Patients</caption>'
print '<thead>'
print '<tr>'
print '<th>Last Name </th>'
print '<th>First Name </th>'
print '<th>SSN </th>'
print '</tr>'
print '</thead>'
print '<tbody>'

for lname,fname,ssn in cursor:
    print '<tr>'
    print '<td>'+ lname+ '</td>'
    print '<td>'+ fname+ '</td>'
    print '<td>'+ ssn+ '</td>'
    print '</tr>'

print '</tbody>'


print '</body>'
