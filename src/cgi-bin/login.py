#!/usr/bin/python
# initial draft of login page

# Author: Ben Metzger
# bmetzger97@gmail.com

# created using python 3.7.X, untested with other versions, your mileage will varry
# documentation:
# https://docs.python.org/3/library/cgi.html

import mysql.connector
import datetime
import cgi
import cgitb
cgitb.enable() #enable error logging in browser, we probably want this on for a while
# cgitb.enable(display=0, logdir="/path/to/logdir") # if you prefer log files
from cgilib import loginlib

print("Content-Type: text/html") #required header line
result = loginlib.verify_login()
form = cgi.FieldStorage()
if "uname" not in form or "pass" not in form:
    print("\n\n")
    print("<H1>Error</H2>\n" +
        "You need to enter a username and password to log in\n" +
        "<a href=/login.html>return to login page</a>")
else:
    password = form.getvalue("pass")
    user = form.getvalue("uname")

    result = loginlib.check_password(password, user)

    if result is not None:
        (ssn, role, user) = result
        cookie = loginlib.init_login(ssn, role, user)
        print(cookie)
        print("Location: http://127.0.0.1/cgi-bin/cookie_test.py")
        print("\n\n")
        print("have a cookie!")
    else:
        print("\n\n")
        print("<H1>Error</H2>\n" +
            "Invalid username and password, please try again\n" +
            "<a href=/login.html>return to login page</a>")


    

    #print("stuffs")
    
