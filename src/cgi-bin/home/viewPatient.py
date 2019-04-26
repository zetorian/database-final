#!/usr/bin/python2

# Import modules for CGI handling and mysql
import cgi, cgitb
import os
import Cookie
import mysql.connector

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
patientSSN = form.getvalue('ssn')
cnx = mysql.connector.connect(user='root',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
cursor.execute("USE EMR;")

print "Content-type:text/html\r\n\r\n"
print '<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>'

query='select lname,fname from patient where ssn ='+patientSSN+';'
cursor.execute(query);

print '<table><caption>Patient Details</caption>'
print '<thead>'
print '<tr>'
print '<th>Last Name </th>'
print '<th>First Name </th>'
print '<th>SSN </th>'
print '</tr>'
print '</thead>'
print '<tbody>'

for lname, fname in cursor:
    print '<tr>'
    print '<td>'+ lname+ '</td>'
    print '<td>'+ fname+ '</td>'
    print '</tr>'

print '</tbody>'

print '<br />'
print '<br />'

print '<table><caption>Appointment History</caption>'
print '<thead>'
print '<tr>'
print '<th>Date/Time</th>'
print '<th>Location</th>'
print '<th>Doctor</th>'
print '</tr>'
print '</thead>'
print '<tbody>'

print '</tbody>'

print '<br />'
print '<br />'

print '<table><caption>Procedure History</caption>'
print '<thead>'
print '<tr>'
print '<th>Date/Time</th>'
print '<th>Location</th>'
print '<th>Doctor</th>'
print '<th>Procedure Type</th>'
print '<th>ID</th>'
print '</tr>'
print '</thead>'
print '<tbody>'

print '</tbody>'

print '<br />'
print '<br />'

print '<table><caption>Prescription History</caption>'
print '<thead>'
print '<tr>'
print '<th>Date</th>'
print '<th>ID</th>'
print '<th>Expires</th>'
print '<th>Drug Name</th>'
print '<th>Doctor</th>'
print '</tr>'
print '</thead>'
print '<tbody>'


print '</tbody>'

print '<br />'
print '<br />'
