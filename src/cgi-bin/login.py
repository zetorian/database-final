#!/usr/bin/python
# initial draft of login page

# Author: Ben Metzger
# bmetzger97@gmail.com

# created using python 3.7.X, untested with other versions, your mileage will varry
# documentation:
# https://docs.python.org/3/library/cgi.html

import msql.connector

import cgi
import cgitb
cgitb.enable() #enable error logging in browser, we probably want this on for a while
# cgitb.enable(display=0, logdir="/path/to/logdir") # if you prefer log files

print("Content-Type: text/html\n\n") #required header line

form = cgi.FieldStorage()
if "uname" not in form or "pass" not in form:
    print("<H1>Error</H2>\n" +
        "could not log in\n" +
        "<a href=/login.html>return to login page</a>")

result = _check_pass()

def _check_pass(p)
    
    
