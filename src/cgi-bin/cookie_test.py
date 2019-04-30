#!/usr/bin/python
# initial draft of login page

# Author: Ben Metzger
# bmetzger97@gmail.com

# created using python 3.7.X, untested with other versions, your mileage will varry
# documentation:
# https://docs.python.org/3/library/cgi.html

import cgi
import cgitb
cgitb.enable() #enable error logging in browser, we probably want this on for a while
# cgitb.enable(display=0, logdir="/path/to/logdir") # if you prefer log files
from cgilib import loginlib


print("Content-Type: text/html") #required header line

#print("yay?")
result = loginlib.verify_login()
if result is not None:
    (ssn, role, user) = result
    if role == "nurse":
        print("Location: http://127.0.0.1/cgi-bin/home/homeNurse.py")
    if role == "doctor":
        print("Location: http://127.0.0.1/cgi-bin/home/homeDoc.py")
    if role == "patient":
        print("Location: http://127.0.0.1/cgi-bin/home/homePatient.py")

print("\n\n\n you probably shouldn't see this page, like, ever. this is an oops")
