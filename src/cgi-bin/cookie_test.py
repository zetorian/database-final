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


print("Content-Type: text/html\n\n") #required header line

print("yay?")
result = loginlib.verify_login()
print(result)

