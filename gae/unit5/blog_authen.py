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


def users_key(group = 'default'):
  return db.Key.from_path('users', group)

class User(db.Model):
  username = db.StringProperty(required = True)
  pw_hash = db.StringProperty(required = True)
  email = db.EmailProperty()

  @classmethod
  def by_id(cls, uid):
    return User.get_by_id(uid, parent = users_key())

  @classmethod
  def by_username(cls, username):
    u = User.all().filter('username = ', username).get()
    return u

  @classmethod
  def register(cls, username, pw, email = None):
    pw_hash = hashutil.make_pw_hash(username, pw)
    return User(parent = users_key(),
                username = username,
                pw_hash = pw_hash,
                email = email)

  @classmethod
  def login(cls, username, pw):
    u = cls.by_username(username)
    if u and hashutil.valid_pw(username, pw, u.pw_hash):
      return u

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

  def set_secure_cookie(self, name, val):

    self.response.headers.add_header('Set-Cookie', 
      '%(name)s=%(val)s' % {'name': name,
                            'val': hashutil.make_secure_val(val)})
  def read_secure_cookie(self, name):
    cookie_str = self.request.cookies.get(name)
    if cookie_str:
        val = hashutil.check_secure_val(cookie_str)
        return val
  
  def login(self, user):
    self.set_secure_cookie('user_id', str(user.key().id()))

  def logout(self):
    #self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    self.response.headers.add_header('Set-Cookie', 'user_id=;')

  def initialize(self, *a, **kw):
    webapp2.RequestHandler.initialize(self, *a, **kw)
    uid = self.read_secure_cookie('user_id')
    self.user = uid and User.by_id(int(uid))

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

    if User.by_username(output_username):
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

      user = User.register(username=output_username, 
                           pw=output_password,
                           email=output_email) 
      user.put()
      self.login(user)
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
    if self.user:
      self.redirect(APP_PATH + CORE_PATH)
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

      err_signin = "User does not exists or password does not match. Try again."

      user = User.login(username=output_username, 
                        pw=output_password)
      if user:
        self.login(user)
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
    self.logout()
    self.redirect(APP_PATH + "/signup")

class WelcomePage(Handler):
  def render_page(self, username):
    self.render("welcome.html", username = username)

  def get(self):
    if self.user:
      self.render_page(self.user.username)
    else:
      self.redirect(APP_PATH + "/signup")


