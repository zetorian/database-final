#!/usr/bin/python

#
#Author: Derek Popowski
#derek.a.popowski@und.edu
#Script to generate the database for CSCI 455 final project
#

#python tableSetup.py [username]
#this script assumes no password for the given user

# imports
# need to pip install mysql-connector-pyton

import mysql.connector
import sys

#connect to mysql running on local hust with a given user

cnx = mysql.connector.connect(user=sys.argv[1],password='',host='localhost')
cursor = cnx.cursor(buffered=True)

#this purges the old one so we can test new build
# do this if you need to run multiple times

#print ('drop database "EMR"')
#query="drop database EMR"
#cursor.execute(query)


# this creates the database
print ('creating database "EMR"')
query="create database EMR"
cursor.execute(query)

#use the new database
query="use EMR"
cursor.execute(query)


table = ['doctor','patient','nurse','login','insuranceCo','Appointment','hospital','procedures','consent','presciption','pharmacy','bill' ]
cols = ["ssn VARCHAR(9), lname VARCHAR(255), fname VARCHAR(255), phone VARCHAR(11), speciality VARCHAR(255), hospital VARCHAR(150), address VARCHAR(255)",
        "ssn VARCHAR(9), lname VARCHAR(255), fname VARCHAR(255), phone VARCHAR(11), address VARCHAR(255), primaryDoctor VARCHAR(9), insuranceCo VARCHAR(150)",
        "ssn VARCHAR(9), lname VARCHAR(255), fname VARCHAR(255), phone VARCHAR(11), address VARCHAR(255), hospital int",
        "login VARCHAR(150), passwordHash VARCHAR(255), ssn VARCHAR(9), level INT",
        "name VARCHAR(150), phone VARCHAR(11), address VARCHAR(255)",
        "dateTime DATETIME, location VARCHAR(255), doctor VARCHAR(9), patient VARCHAR(9), paid DECIMAL(7,2), ammountBilled DECIMAL(7,2)",
        "id INT AUTO_INCREMENT, name VARCHAR(255), phone VARCHAR(11), address VARCHAR(255), PRIMARY KEY(id)",
        "id INT AUTO_INCREMENT, procedureName VARCHAR(255), dateTime DATETIME, doctor VARCHAR(9), patient VARCHAR(9), results TEXT, paid DECIMAL(7,2), amountBilled DECIMAL(7,2), PRIMARY KEY(id)",
        "id INT AUTO_INCREMENT, patient VARCHAR(9), transferTo VARCHAR(255), signed BOOLEAN, approved BOOLEAN, PRIMARY KEY(id)",
        "prescriptionNum INT AUTO_INCREMENT, patient VARCHAR(9), doctor VARCHAR(9), date DATETIME, expires DATETIME, PRIMARY KEY(prescriptionNum)",
        "name VARCHAR(150), phone VARCHAR(11), address VARCHAR(255)",
        "patient VARCHAR(9), balance DECIMAL(7,2)"]

for i in range(12): 
    query="create table " + table[i] +  "(" + cols[i] + ");"

#    print('\nDEBUGQUERY: ' + query)

    cursor.execute(query)
    print('\ncreating ' + table[i])
    print('with columns ' + cols[i])
    
Pkeys = ["ADD PRIMARY KEY (ssn)",
        "ADD PRIMARY KEY (ssn)",
        "ADD PRIMARY KEY (ssn)",
        "ADD PRIMARY KEY (login)",
        "ADD PRIMARY KEY (name)",
        "ADD PRIMARY KEY (dateTime, doctor)",
        "",
        "",
        "",
        "",
        "ADD PRIMARY KEY (name)",
        "ADD PRIMARY KEY (patient)"]

Fkeys = ["",
        "ADD (FOREIGN KEY (primaryDoctor) REFERENCES doctor(ssn), FOREIGN KEY(insuranceCo) REFERENCES insuranceCo(name))",
         "ADD FOREIGN KEY (hospital) REFERENCES hospital(id)",
         "ADD FOREIGN KEY (ssn) REFERENCES doctor(ssn)",
        "",
        "ADD (FOREIGN KEY (doctor) REFERENCES doctor(ssn), FOREIGN KEY (patient) REFERENCES patient(ssn))",
        "",
        "ADD (FOREIGN KEY (patient) REFERENCES patient(ssn), FOREIGN KEY (doctor) REFERENCES doctor(ssn))",
        "ADD FOREIGN KEY (patient) REFERENCES patient(ssn)",
        "ADD (FOREIGN KEY (patient) REFERENCES patient(ssn), FOREIGN KEY (doctor) REFERENCES doctor(ssn))",
        "",
        ""]

for i in range(12):
    if Pkeys[i] != "":
        print('\naltering primary keys for ' + table[i])
        query = "alter table " + table[i]+ " " + Pkeys[i] + ';'

#        print('DEBUGQUERY: ' + query)
    
        cursor.execute(query)

for i in range(12):
    if Fkeys[i] != "":
        print('\naltering foreign keys for ' + table[i])
        query = "alter table " + table[i]+ " " + Fkeys[i] + ';'

#        print('DEBUGQUERY: ' + query)
    
        cursor.execute(query)
