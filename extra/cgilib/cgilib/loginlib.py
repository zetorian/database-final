from os import environ
from pymacaroons import Macaroon, Verifier
import cookies

def verify_login():
    if "HTTP_COOKIE" in environ:
        C = cookies.SimpleCookie(environ['HTTP_COOKIE'])
        C.load()
        sdata = C["EMR-login-state"].value
        mac = Macaroon.deserialize(sdata)
        
        if _verify_macaroon(mac) == True:
            role = mac.caveats[0].caveat_id.split(' = ')[1]
            return (mac.identifier(), role)
    return None

def _verify_macaroon(mac):
    v = Verifier()
    #verify the role is valid
    v.satisfy_general(_role_verification)
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


#in the scope of a real system, this would use a random, unique ID number, this is not a real system and creating ID numbers was considered out of scope
def _gen_macaroon(ssn, role):
    f = open("/var/EMR/secret_key", "r")
    if f.mode == 'r':
        secret_key = f.read()
        mac = Macaroon(
                location="http://127.0.0.1", #again, this should not be set to local host, but this is a demo, not a full system.
                identifier=ssn,
                key=secret_key
                )
        mac.add_first_party_caveat('role = ' + role)
        return mac
    else:
        print("keyfile not found")
        return None

#check_active_login()
