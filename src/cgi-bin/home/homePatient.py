#!/usr/bin/python

# Import modules for CGI handling and mysql
import cgi, cgitb
import os
import mysql.connector
from cgilib import loginlib


# Get data from fields
cnx = mysql.connector.connect(user='cs',password='',host='localhost')
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
cursor.execute("USE EMR;")

print("Content-type: text/html")
#
result = loginlib.verify_login()
user = ""
userType='patient'
userSSN='100000179'
if result is not None:
    (ssn, role, user) = result
    userType = role
    userSSN = ssn
else:
    print("Location: /html/login.html")

print('\n\n<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>')

#if we got here the user must be a patient
print('<!DOCTYPE html><html><head><style>table, th, td {  border: 1px solid black;}</style></head>')
print('<h1>')
print('You are logged in as ' + user)
print('</h1>\n')
print('<body>\n')

#
# schedule a new appointment
#

print('<form action="addappointment.py" method="post">')
print('<input type="submit" value="Schedule an Appointment" />')
print('</form>')


query='select lname,fname,ssn,address,phone,primaryDoctor from patient where ssn ='+userSSN+';'
cursor.execute(query);

print('<table><caption>Your Details</caption>')
print('<thead>')
print('<tr>')
print('<th>Last Name </th>')
print('<th>First Name </th>')
print('<th>SSN </th>')
print('<th>Address </th>')
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

print('<table><caption>Your Appointment History</caption>')
print('<thead>')
print('<tr>')
print('<th>Date/Time</th>')
print('<th>Location</th>')
print('<th>Doctor</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select dateTime,location,doctor from Appointment where patient ='+userSSN+';'
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

print('<table><caption>Your Procedure History</caption>')
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

query='select dateTime,doctor,id,procedureName from procedures where patient ='+userSSN+';'
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

print('<table><caption>Your Prescription History</caption>')
print('<thead>')
print('<tr>')
print('<th>Date</th>')
print('<th>ID</th>')
print('<th>Expires</th>')
print('<th>Doctor</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select doctor,prescriptionNum,date,expires from presciption where patient ='+userSSN+';'
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

print('<table><caption>Your Billing Details</caption>')
print('<thead>')
print('<tr>')
print('<th>Amount Due</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

query='select balance from bill where patient='+userSSN+';'
cursor.execute(query);

for balance in cursor:
    print('<tr>')
    print('<th>'+balance+'</th>')
    print('</tr>')
    
print('</tbody>')

print('<br />')
print('<br />')

print('<table><caption>Your Doctor</caption>')
print('<thead>')
print('<tr>')
print('<th>First Name</th>')
print('<th>Last Name</th>')
print('<th>Hospital</th>')
print('<th>Phone</th>')
print('</tr>')
print('</thead>')
print('<tbody>')

cursor.execute("select primaryDoctor from patient where ssn ="+userSSN+ ";")
for result in cursor:
    doctor=result
    
query='select fname,lname,hospital,phone from doctor where ssn ='+doctor+';'
cursor.execute(query);

for fname,lname,hospital,phone in cursor:
    print('<tr>')
    print('<th>'+fname+'</th>')
    print('<th>'+lname+'</th>')
    print('<th>'+hospital+'</th>')
    print('<th>'+phone+'</th>')
    print('</tr>')

print('</tbody>')

print('<br />')
print('<br />')
