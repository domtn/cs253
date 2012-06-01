import re
  
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def is_username_valid(username):
  return USER_RE.match(username)

def is_password_valid(password):
  return PWD_RE.match(password)

def is_email_valid(email):
  if email == "":
  	return True
  return EMAIL_RE.match(email)
