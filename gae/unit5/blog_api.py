# "created": "Wed May 2 18:33:55 2012"
# "last_modified": "Wed May 2 18:33:55 2012"

# Content-Type: application/json; charset=UTF-8
import os
import webapp2
import jinja2
import datetime
import json

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

date_format = "%A %B %d %H:%M:%S %Y "

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

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

class Posts(Handler):
  def render_posts(self, format=""):
    posts = db.GqlQuery("SELECT * FROM BlogPost \
                     ORDER BY created DESC")
    decor_posts = []
    for post in posts:
      post.permalink = "/unit5/blog/" + str(post.key().id())
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
      self.render("posts.html", posts=decor_posts)

  def get(self, format):
    self.render_posts(format)

class Post(Handler):
  def render_post(self, post_id="", format=""):
    post = BlogPost.get_by_id(long(post_id))

    if post:
      post.permalink = "/unit5/blog/" + str(post.key().id())
      post.lastUpdated = post.created.strftime(format)
      if format==".json":
        json_post = ({'subject': post.subject,
                      'content': post.content,
                      'created': post.created.strftime(date_format),
                      'last_modified': post.last_modified.strftime(date_format)
                    })
        self.render_json(json_post)
      else:
        self.render("post.html", post=post)
    else:
      error = "Could not find the post you wanted to read!"
      if format==".json":
        self.render_json({})
      else:
        self.render("post.html", post=None, error=error)

  def get(self, post_id, format):
    self.render_post(post_id=post_id, format=format)

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
      self.redirect("/unit5/blog/" + str(a.key().id()))
    else:
      error = "we need both a subject and some content"
      self.render_newpost(subject, content, error)



