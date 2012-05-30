import hashlib

import hmac

    
SEPARATOR = "|"

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'imsosecret'

def hmac_str(s):
    return hmac.new(SECRET, s).hexdigest()

def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_salt():
    return ''.join(random.choice(string.letters + string.digits) for x in range(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash(name, pw, salt=""):
    if salt == "":
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt_component = h.split(",")[1];
    if salt_component:
        if make_pw_hash(name, pw, salt_component) == h:
            return True

    
def make_secure_val(s):
    return "%s%s%s" % (s, SEPARATOR, hmac_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hmac_str(s) == HASH, otherwise None 

def check_secure_val(h):
    if h and (SEPARATOR in h):
        first_comma_pos = h.index(SEPARATOR)
        val = h[0:first_comma_pos]
        hashed = h[first_comma_pos+1:len(h)]
        if hmac_str(val) == hashed:
            return val
        else:
            return None