import os
import webapp2
import jinja2
import datetime
import signuputil
from util import html_util
import hashutil

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

APP_PATH = "/unit5/blog"
CORE_PATH = "/welcome"

class User(db.Model):
  username = db.StringProperty(required = True)
  password_hash = db.StringProperty(required = True)
  email = db.EmailProperty(required = False)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class SignupPage(Handler):
  def render_page(self, username="", err_username="",
                  password="", err_password="",
                  verify="", err_verify="", 
                  email="", err_email=""):
    self.render("signup.html", username=username, err_username=err_username,
                               password=password, err_password=err_password,
                               verify=verify, err_verify=err_verify,
                               email=email, err_email=err_email)

  def get(self):
    self.render_page()

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

    query = "SELECT * FROM User \
               WHERE username = '" + output_username + "'"
    users = db.GqlQuery(query)
    if users.count() > 0:
      err_username = "Username already taken"
    
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

      if output_email == "":
        output_email = None
      user = User(username = output_username, 
                  password_hash = hashutil.make_pw_hash(output_username, output_password), 
                  email=output_email)
      user.put()
      user_id = user.key().id()
      self.response.headers.add_header('Set-Cookie', 'user_id=%s' % hashutil.make_secure_val(str(user_id)))
      self.redirect(APP_PATH + CORE_PATH)
    else:
      self.render_page(output_username, err_username,
                      output_password, err_password,
                      output_verify, err_verify,
                      output_email, err_email)

class LoginPage(Handler):
  def render_page(self, err_signin="", 
                    username="", err_username="", 
                    password="", err_password=""):
    self.render("signin.html", err_signin = err_signin, 
                               username=username, err_username=err_username,
                               password=password, err_password=err_password)
  def get(self):
    self.render_page()

  def post(self):
    input_username = self.request.get('username')
    input_password = self.request.get('password')

    err_username = ""
    err_password = ""
    err_signin = ""

    output_username = html_util.escape_html(input_username)
    output_password = input_password

    if not signuputil.is_username_valid(input_username):
      err_username = "Invalid username"
    
    if not signuputil.is_password_valid(input_password):
      err_password = "Invalid password"
      output_password = ""


    if err_username == "" and \
       err_password == "":
      query = "SELECT * FROM User \
               WHERE username = '" + output_username + "'"
      users = db.GqlQuery(query)

      err_signin = "User does not exists or password does not match. Try again."

      if users.count() > 0 and \
         hashutil.valid_pw(users[0].username, output_password, users[0].password_hash):
        user_id = users[0].key().id()
        self.response.headers.add_header('Set-Cookie', 'user_id=%s' % hashutil.make_secure_val(str(user_id)))
        self.redirect(APP_PATH + CORE_PATH)
      else:
        self.render_page(err_signin,
                     output_username, err_username,
                     output_password, err_password)
    else:
      self.render_page(err_signin,
                     output_username, err_username,
                     output_password, err_password)
      

class LogoutPage(Handler):
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
    #self.response.headers.add_header('Set-Cookie', 'user_id=;')
    self.redirect(APP_PATH + "/signup")

class WelcomePage(Handler):
  def render_page(self, username):
    self.render("welcome.html", username = username)

  def get(self):
    user_id_cookie_str = self.request.cookies.get('user_id')

    username = ""
    if user_id_cookie_str:
        user_id = hashutil.check_secure_val(user_id_cookie_str)
        if user_id:
            user = User.get_by_id(long(user_id))
            if user:
              username = user.username
    if username == "":
      self.redirect(APP_PATH + "/signup")
    else:
      self.render_page(username)


