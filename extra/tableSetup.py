#!/usr/bin/python2

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
import random
import hashlib

#connect to mysql running on local hust with a given user

cnx = mysql.connector.connect(user=sys.argv[1],password='',host='localhost')
cursor = cnx.cursor(buffered=True)

#this purges the old one so we can test new build
# do this if you need to run multiple times
#comment this out if this is the first time run


print ('drop database "EMR"')
query="drop database EMR"
cursor.execute(query)


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
        "ssn VARCHAR(9), lname VARCHAR(255), fname VARCHAR(255), phone VARCHAR(11), address VARCHAR(255), hospital INT",
        "login VARCHAR(150), passwordHash VARCHAR(255), ssn VARCHAR(9)",
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
        "",
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


#
# Here we open all the list files for data generation
#
#

hospitalFN=open("hospital.txt","r")
pharmacyFN=open("pharmacy.txt","r")
listFN=open("first-names.txt","r")
listLN=open("last-names.txt","r")
listAddr=open("addresses.txt","r")
listIns=open("insuranceCos.txt","r")


# Create all the lists and fill with the data from the files

fnames=[]
fnames=listFN.read().splitlines()

lnames=[]
lnames=listLN.read().splitlines()
i=0
for name in lnames:
    lnames[i]=lnames[i].capitalize()
    i+=1

hospitals=[]
hospitals=hospitalFN.read().splitlines()

pharmacies=[]
pharmacies=pharmacyFN.read().splitlines()

insuranceCo=[]
insuranceCo=listIns.read().splitlines()

address=[]
address=listAddr.read().splitlines()
nextAddr=0


# just using an increment to imitate phone numbers and ensure they are distinct

nextPhone=5551111111

#
# creating the hospitals, pharmacies and insurance companies
# first since they do not have any foreign keys
#

for i in range(3):
    print "adding in the three test hospitals"
    query= "INSERT INTO hospital (name, phone, address) VALUES (%s,%s,%s);"
    args=(hospitals[i],str(nextPhone),address[nextAddr])
    nextPhone+=1
    nextAddr+=1
#    print "DEBUGQUERY: " + query
    cursor.execute(query,args)
    
for i in range(3):
    print "adding in the three test pharmacies"
    query= "INSERT INTO pharmacy (name, phone, address) VALUES (%s,%s,%s);"
    args=(pharmacies[i],str(nextPhone),address[nextAddr])
    nextPhone+=1
    nextAddr+=1
#    print "DEBUGQUERY: " + query
    cursor.execute(query,args)

for i in range(3):
    print "adding in the three test insurance"
    query= "INSERT INTO insuranceCo (name, phone, address) VALUES (%s,%s,%s);"
    args=(insuranceCo[i],str(nextPhone),address[nextAddr])
    nextPhone+=1
    nextAddr+=1
#    print "DEBUGQUERY: " + query
    cursor.execute(query,args)

#
# here we will create some doctors
# will create -TODO-  add specialty 
# SSNs will be consecutive and names randomized from the two word lists
#

for i in range(100000000,100000030):
    print "adding doctor#: " + str(i-100000000)
    query = "INSERT INTO doctor (ssn, fname, lname, phone, address,hospital) VALUES (%s,%s,%s,%s,%s,%s);"
    args = (str(i),fnames[random.randint(0,4944)],lnames[random.randint(0,663)],str(nextPhone),address[nextAddr],hospitals[random.randint(0,2)])
#    print "DEBUGQUERY: " + query
    nextPhone+=1
    nextAddr+=1
    cursor.execute(query,args)

#
# here is the same for patients
# creating 150
#
docSSNs=[] # for primary doctor
query="SELECT ssn FROM doctor;"
cursor.execute(query)
for ssn, in cursor:
    docSSNs.append(ssn)
    
for i in range(100000030,100000180):
    print "adding patient#: " + str(i-100000030)
    query = "INSERT INTO patient (ssn, fname, lname, phone, address, insuranceCo,primaryDoctor) VALUES (%s,%s,%s,%s,%s,%s,%s);"
    args = (str(i),fnames[random.randint(0,4944)],lnames[random.randint(0,663)],str(nextPhone),address[nextAddr],insuranceCo[random.randint(0,2)],docSSNs[random.randint(0,29)])
    print "DEBUGQUERY: " + query
    nextPhone+=1
    nextAddr+=1
    cursor.execute(query,args)

#
# here is for nurses
# create 30 
#

for i in range(100000180,100000210):
    print "adding nurse#: " + str(i-100000000)
    query = "INSERT INTO nurse (ssn, fname, lname, phone, address,hospital) VALUES (%s,%s,%s,%s,%s,%s);"
    args = (str(i),fnames[random.randint(0,4944)],lnames[random.randint(0,663)],str(nextPhone),address[nextAddr],str(random.randint(1,3)))
#    print "DEBUGQUERY: " + query
    nextPhone+=1
    nextAddr+=1
    cursor.execute(query,args)

#
# import password lists - users will be generated from the doctor/patient/nurse tables first.last names
# generate the password hashes and insert into the login table
#
passwords=[]
userNames=[]
passwdFN=open("darkweb2017-top1000.txt","r")
passwords=passwdFN.read().splitlines()
hashes=[]

# This was the test for the password hashing

#for passwd in passwords:
#    hash = hashlib.sha1(passwd)
#    hashes.append(hash.hexdigest())
#    print(passwd + ":" + hash.hexdigest())
    
query = "SELECT fname,lname,ssn FROM doctor;"
cursor.execute(query)
users={}
for fname,lname,ssn in cursor:
    users[fname + "." + lname] = ssn
query = "SELECT fname,lname,ssn FROM patient;"
cursor.execute(query)
for fname,lname,ssn in cursor:
    users[fname + "." + lname] = ssn
query = "SELECT fname,lname,ssn FROM nurse;"
cursor.execute(query)
for fname,lname,ssn in cursor:
    users[fname + "." + lname] = ssn
    
# This was for debug of username creation    
    
#for user in users:
#    print(user)

# open/create the user/password file they will be in the form user:password
userpassFN = open("user_passwd.txt","w+")

#
# this gens the users and the userpassword list
#
for user in users:
    passwd=passwords[random.randint(0,976)]
    hashed_pass = hashlib.sha1(passwd.encode("ascii"))
    filestr= str(user + ":" + passwd)
    userpassFN.write(filestr+'\n')
    query="INSERT INTO login (login, passwordHash,ssn) VALUES ('" + user + "','" + hashed_pass.hexdigest() + "','" + users[user] +"');"
#    print("DEBUGQUERY: " + query)
    print("CREATING USER: " + user + " with hash : " + hashed_pass.hexdigest() + " and ssn : " + users[user])
    cursor.execute(query)

#
# commit and close
#
cnx.commit()
cursor.close()
cnx.close()
