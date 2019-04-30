import datetime
import mysql.connector
from os import environ
from pymacaroons import Macaroon, Verifier
from http import cookies
import hashlib

def verify_login():
    if "HTTP_COOKIE" in environ:
        C = cookies.SimpleCookie()
        C.load(environ['HTTP_COOKIE'])
        sdata = C["EMR-login-state"].value
        mac = Macaroon.deserialize(sdata)
        
        if _verify_macaroon(mac) == True:
            role = ""
            user = ""
            for m in mac.caveats:
                if m.caveat_id.split(' = ')[0] == "role":
                    role = m.caveat_id.split(' = ')[1]
                if m.caveat_id.split(' = ')[0] == "user":
                    user = m.caveat_id.split(' = ')[1]
            return (mac.identifier, role, user)
    return None

def init_login(ssn, role, user):
    mac = _gen_macaroon(ssn, role, user)
    sdata = mac.serialize()
    C = cookies.SimpleCookie()
    C["EMR-login-state"] = sdata
    return C

def check_password(input_pass, user):
    cnx = mysql.connector.connect(user="cs", database="EMR")
    cursor = cnx.cursor()
    query = ("SELECT passwordHash, ssn FROM EMR.login "
            "WHERE login = '" + user + "'")
    cursor.execute(query)

    input_pass_hashed = hashlib.sha1(input_pass.encode("ascii"))

    for (passwordHash, ssn) in cursor:
        if passwordHash == input_pass_hashed.hexdigest():
            role = lookup_role(ssn)
            return (ssn, role, user)

    return None

def lookup_role(ssn):
    cnx = mysql.connector.connect(user="cs", database="EMR")
    cursor = cnx.cursor()
    query = ("SELECT ssn FROM EMR.doctor "
            "WHERE ssn = '" + ssn + "'")
    cursor.execute(query)
    for (ssn) in cursor:
        return "doctor"
    query = ("SELECT ssn FROM EMR.nurse "
            "WHERE ssn = '" + ssn + "'")
    cursor.execute(query)
    for (ssn) in cursor:
        return "nurse"
    query = ("SELECT ssn FROM EMR.patient "
            "WHERE ssn = '" + ssn + "'")
    cursor.execute(query)
    for (ssn) in cursor:
        return "patient"


def _verify_macaroon(mac):
    v = Verifier()
    #verify the role is valid
    v.satisfy_general(_role_verification)
    #verify username is valid, only checks to make sure it only contains ascii, could be improved.
    v.satisfy_general(_user_verification)
    f = open("/var/EMR/secret_key", "r")
    if f.mode == 'r':
        secret_key = f.read()
        return v.verify(mac, secret_key)
    return None

def _role_verification(caveat):
    c = caveat.split(' = ')
    if c[0] != 'role':
        return False
    elif c[1] == 'doctor':
        return True
    elif c[1] == 'nurse':
        return True
    elif c[1] == 'patient':
        return True

    return False

def _user_verification(caveat):
    c = caveat.split(' = ')
    if c[0] != 'user':
        return False
    try:
        c[1].encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

    return False



#in the scope of a real system, this would use a random, unique ID number, this is not a real system and creating ID numbers was considered out of scope
def _gen_macaroon(ssn, role, user):
    f = open("/var/EMR/secret_key", "r")
    if f.mode == 'r':
        secret_key = f.read()
        mac = Macaroon(
                location="http://127.0.0.1", #again, this should not be set to local host, but this is a demo, not a full system.
                identifier=ssn,
                key=secret_key
                )
        mac.add_first_party_caveat('role = ' + role)
        mac.add_first_party_caveat('user = ' + user)
        return mac
    else:
        print("keyfile not found")
        return None

#check_active_login()
