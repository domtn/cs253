import os
import webapp2
import jinja2
import hashutil

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

class MainPage(Handler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'

    visits = 0
    visits_cookie_str = self.request.cookies.get('visits')

    if visits_cookie_str:
        cookie_val = hashutil.check_secure_val(visits_cookie_str)
        if cookie_val:
            visits = int(cookie_val)
    
    visits += 1

    self.response.headers.add_header('Set-Cookie', 'visits=%s' % hashutil.make_secure_val(str(visits)))

    if visits > 10:
        self.write("You are the best ever!")
    else:
        self.write("You've been here %s times!" % visits)