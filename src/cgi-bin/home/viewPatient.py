#!/usr/bin/python3

# Import modules for CGI handling and mysql
import cgi, cgitb
import os
import http.cookies
import mysql.connector

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
patientSSN = form.getvalue('ssn')
cnx = mysql.connector.connect(user='root',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
cursor.execute("USE EMR;")

print("Content-type:text/html\r\n\r\n")
print('<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>')

query='select lname,fname,ssn,address,phone,primaryDoctor from patient where ssn ='+patientSSN+';'
cursor.execute(query);

#
# for directing to the update pages make sure that they are in the same directory
#
print('<form action="addprescription.py" method="post">')
print('<input type="submit" value="Add a Prescription" />')
print('</form>')

print('<form action="addprocedure.py" method="post">')
print('<input type="submit" value="Schedule a Procedure" />')
print('</form>')

print('<form action="addappointment.py" method="post">')
print('<input type="submit" value="Schedule an Appointment" />')
print('</form>')

print('<table><caption>Patient Details</caption>')
print('<thead>')
print('<tr>')
print('<th>Last Name </th>')
print('<th>First Name </th>')
print('<th>SSN </th>')
print('<th>Address</th>')
print('<th>Phone</th>')
print('<th>Primary Doctor</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

for lname, fname,ssn,address,phone,primaryDoctor in cursor:
    print('<tr>')
    print('<td>'+ lname+ '</td>')
    print('<td>'+ fname+ '</td>')
    print('<td>'+ ssn+ '</td>')
    print('<td>'+ address+ '</td>')
    print('<td>'+ phone+ '</td>')
    cursor2.execute('select fname,lname from doctor where ssn ='+primaryDoctor+';')
    for fname, lname in cursor2:
        print('<th>'+fname+' ' +lname+'</th>')
    print('</tr>')

print('</tbody>')

print('<br />')
print('<br />')

print('<table><caption>Appointment History</caption>')
print('<thead>')
print('<tr>')
print('<th>Date/Time</th>')
print('<th>Location</th>')
print('<th>Doctor</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select dateTime,location,doctor from Appointment where patient ='+patientSSN+';'
cursor.execute(query)
for doctor, in cursor:
    cursor2.execute('select fname,lname from doctor where ssn ='+doctor+';')
for dateTime,location in cursor:
    print('<tr>')
    print('<th>'+dateTime+'</th>')
    print('<th>'+location+'</th>')
    for fname,lname in cursor2:
        print('<th>'+fname+' ' +lname+'</th>')
    print('</tr>')

print('</tbody>')

print('<br />')
print('<br />')

print('<table><caption>Procedure History</caption>')
print('<thead>')
print('<tr>')
print('<th>Date/Time</th>')
print('<th>Location</th>')
print('<th>Doctor</th>')
print('<th>Procedure Type</th>')
print('<th>ID</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select dateTime,doctor,id,procedureName from procedures where patient ='+patientSSN+';'
cursor.execute(query);
print('<tr>')
for dateTime,doctor,id,procedureName in cursor:
    print('<th>'+dateTime+'</th>')
    print('<th>'+location+'</th>')
    print('<th>'+doctor+'</th>')
    print('<th>'+procedureName+'</th>')
    print('<th>'+id+'</th>')
print('</tr>')

print('</tbody>')

print('<br />')
print('<br />')

print('<table><caption>Prescription History</caption>')
print('<thead>')
print('<tr>')
print('<th>Date</th>')
print('<th>ID</th>')
print('<th>Expires</th>')
print('<th>Doctor</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select doctor,prescriptionNum,date,expires from presciption where patient ='+patientSSN+';'
cursor.execute(query);
for doctor,prescriptionNum,date,expires in cursor:
    print('<tr>')
    print('<th>'+date+'</th>')
    print('<th>'+prescriptionNum+'</th>')
    print('<th>'+expires+'</th>')
    print('<th>'+doctor+'</th>')
print('</tr>')
print('</tbody>')

print('<br />')
print('<br />')
