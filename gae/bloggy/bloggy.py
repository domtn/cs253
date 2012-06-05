import os
import webapp2
import jinja2
import datetime
import json
import signuputil
from util import html_util
import hashutil

from google.appengine.ext import db


APP_PATH = "/bloggy"
CORE_PATH = "/blog"
SIGN_IN_PATH = "/login"
SIGN_OUT_PATH = "/logout"
SIGN_UP_PATH = "/signup"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

date_format = "%A %B %d %H:%M:%S %Y "

'''
Base Handler class
'''
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
    self.response.headers.add_header('Set-Cookie', 'user_id=;')

  def initialize(self, *a, **kw):
    webapp2.RequestHandler.initialize(self, *a, **kw)
    uid = self.read_secure_cookie('user_id')
    self.user = uid and User.by_id(int(uid))

  def render_json(self, d):
    json_txt = json.dumps(d)
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.write(json_txt)

class BlogPost(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)

class ArchivePost(db.Model):
  subject = db.StringProperty(required=True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  original_id = db.IntegerProperty(required=True)

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


class Posts(Handler):
  def render_posts(self, format="", user=None):
    posts = db.GqlQuery("SELECT * FROM BlogPost \
                     ORDER BY created DESC")
    decor_posts = []
    for post in posts:
      post.permalink = APP_PATH + CORE_PATH + "/" + str(post.key().id())
      post.lastUpdated = post.last_modified.strftime(date_format)
      decor_posts.append(post)

    if format == "/.json":
      json_posts = []
      for post in decor_posts:
        json_posts.append({ 'subject': post.subject,
                            'content': post.content,
                            'created': post.created.strftime(date_format),
                            'last_modified': post.last_modified.strftime(date_format)
                          })
      self.render_json(json_posts)
    else:
      link_to_new_post = None
      link_to_sign_in = None
      link_to_register = None
      link_to_sign_out = None

      if user != None:
        link_to_new_post = APP_PATH + "/blog/newpost"
        link_to_sign_out = APP_PATH + SIGN_OUT_PATH
      else:
        link_to_register = APP_PATH + SIGN_UP_PATH
        link_to_sign_in = APP_PATH + SIGN_IN_PATH

      self.render("posts.html", posts=decor_posts, 
                                link_to_new_post=link_to_new_post,
                                link_to_sign_in=link_to_sign_in,
                                link_to_register=link_to_register,
                                link_to_sign_out=link_to_sign_out)

  def get(self, format):
    self.render_posts(format, self.user)

class Post(Handler):
  def render_post(self, post_id="", format=""):
    post = BlogPost.get_by_id(long(post_id))

    if post:
      post.permalink = APP_PATH + CORE_PATH + "/" + str(post.key().id())
      post.lastUpdated = post.created.strftime(format)
      if format==".json":
        json_post = ({'subject': post.subject,
                      'content': post.content,
                      'created': post.created.strftime(date_format),
                      'last_modified': post.last_modified.strftime(date_format)
                    })
        self.render_json(json_post)
      else:
        self.render("post.html", post=post, link_to_posts=APP_PATH + CORE_PATH)
    else:
      error = "Could not find the post you wanted to read!"
      if format==".json":
        self.render_json({})
      else:
        self.render("post.html", post=None, error=error, link_to_posts=APP_PATH + CORE_PATH)

  def get(self, post_id, format):
    self.render_post(post_id=post_id, format=format)

class NewPost(Handler):
  def render_newpost(self, subject="", content="", error=""):
    self.render("new_post.html", subject=subject, 
                                 content=content, 
                                 error=error, 
                                 link_to_posts=APP_PATH + CORE_PATH)

  def get(self):
    if self.user == None:
      self.redirect(APP_PATH + SIGN_IN_PATH)
    self.render_newpost()

  def post(self):
    if self.user == None:
      self.redirect(APP_PATH + SIGN_IN_PATH)
    subject = self.request.get("subject")
    content = self.request.get("content")

    if subject and content:
      a = BlogPost(subject = subject, content = content)
      a.put()
      self.redirect(APP_PATH + CORE_PATH + "/" + str(a.key().id()))
    else:
      error = "we need both a subject and some content"
      self.render_newpost(subject, content, error)


class SignupPage(Handler):
  def render_page(self, username="", err_username="",
                  password="", err_password="",
                  verify="", err_verify="", 
                  email="", err_email=""):
    self.render("signup.html", username=username, err_username=err_username,
                               password=password, err_password=err_password,
                               verify=verify, err_verify=err_verify,
                               email=email, err_email=err_email,
                               link_to_sign_in=APP_PATH + SIGN_IN_PATH)

  def get(self):
    self.logout()
    self.render_page()

  def post(self):
    self.logout()
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
      if input_email == "":
        output_email = None
      err_email = "Invalid email"

    if err_username == "" and \
       err_password == "" and \
       err_verify == "" and \
       err_email == "":
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
                               password=password, err_password=err_password, 
                               link_to_register=APP_PATH + SIGN_UP_PATH)
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
    self.redirect(APP_PATH + CORE_PATH)

