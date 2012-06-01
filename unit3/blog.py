import os
import webapp2
import jinja2

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


class BlogPost(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
  def render_posts(self):
    posts = db.GqlQuery("SELECT * FROM BlogPost \
                     ORDER BY created DESC")
    self.render("posts.html", posts=posts)

  def get(self):
    self.render_posts()

class NewPost(Handler):
  def render_newpost(self, subject="", content="", error=""):
    self.render("new_post.html", subject=subject, content=content, error=error)

  def get(self):
    self.render_newpost()

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")

    if subject and content:
      a = BlogPost(subject = subject, content = content)
      a.put()

      self.redirect("/unit3/blog")
    else:
      error = "we need both a subject and some content"
      self.render_newpost(subject, content, error)



