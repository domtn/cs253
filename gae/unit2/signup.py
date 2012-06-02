import webapp2
from util import html_util
import signuputil
import urllib

signup_form="""
<form method="post">
  <h2>Signup</h2>
  <label>
    Username
    <input type="text" name="username" value="%(username)s">
    <span style="color:red">%(err_username)s</span>
  </label>
  <br>
  <label>
    Password
    <input type="password" name="password" value="%(password)s">
    <span style="color:red">%(err_password)s</span>
  </label>
  <br>  
  <label>
    Verify Password
    <input type="password" name="verify" value="%(verify)s">
    <span style="color:red">%(err_verify)s</span>
  </label>
  <br>
  <label>
    Email (optional)
    <input type="text" name="email" value="%(email)s">
    <span style="color:red">%(err_email)s</span>
  </label>
  
  <br>
  <input type="submit">
</form>
"""

welcome_form = """
  <h2>Welcome, %(username)s</h2>
"""
class MainPage(webapp2.RequestHandler):
  def write_form(self, username="",
                       err_username="", 
                       password="", 
                       err_password="", 
                       verify="", 
                       err_verify="",
                       email="",
                       err_email=""):
    self.response.out.write(signup_form % {"username": username, 
                                    "err_username": err_username,
                                    "password": password,
                                    "err_password": err_password,
                                    "verify": verify,
                                    "err_verify": err_verify,
                                    "email": email,
                                    "err_email": err_email})

  def get(self):
    self.write_form()

  def post(self):
    input_username = self.request.get('username')
    input_password = self.request.get('password')
    input_verify = self.request.get('verify')
    input_email = self.request.get('email')

    err_username = ""
    err_password = ""
    err_verify = ""
    err_email = ""

    output_username = html_util.escape_html(input_username)
    output_password = input_password
    output_verify = input_verify
    output_email = html_util.escape_html(input_email)

    if not signuputil.is_username_valid(input_username):
      err_username = "Invalid username"
    
    if not signuputil.is_password_valid(input_password):
      err_password = "Invalid password"
      output_password = ""
      output_verify = ""

    if input_password != input_verify:
      err_verify = "Does not match the password you entered"

    if not signuputil.is_email_valid(input_email):
      err_email = "Invalid email"

    if err_username == "" and \
       err_password == "" and \
       err_verify == "" and \
       err_email == "":
      newurl = 'welcome?' + urllib.urlencode({'username':output_username})
      self.redirect(newurl)
    else:
      self.write_form(output_username, err_username,
                      output_password, err_password,
                      output_verify, err_verify,
                      output_email, err_email)


class WelcomePage(webapp2.RequestHandler):
  def write_form(self, username=""):
    self.response.out.write(welcome_form % {"username": username})
  
  def get(self):
    username = self.request.get('username')
    if signuputil.is_username_valid(username):
      self.write_form(username)
    else:
      self.redirect('signup')