import webapp2
from unit1 import dateform
from unit2 import rot13
from unit2 import signup
from unit3 import asciichan
from unit3 import blog
from unit4 import play

form="""
<h2>Welcome to Web Application Engineering</h2>
<br>
<img src="https://developers.google.com/appengine/images/appengine-silver-120x30.gif" 
alt="Powered by Google App Engine" />
"""

class MainPage(webapp2.RequestHandler):
  def write_form(self):
    self.response.out.write(form)

  def get(self):
    self.write_form()

  def post(self):
    self.write_form()

app = webapp2.WSGIApplication([
                  webapp2.Route(r'/', handler=MainPage),
                  webapp2.Route(r'/unit1/dateform', handler=dateform.MainPage),
                  webapp2.Route(r'/unit1/thanks', handler=dateform.ThanksPage), 
                  webapp2.Route(r'/unit2/rot13', handler=rot13.MainPage),
                  webapp2.Route(r'/unit2/signup', handler=signup.MainPage),
                  webapp2.Route(r'/unit2/welcome', handler=signup.WelcomePage),
                  webapp2.Route(r'/unit3/asciichan', handler=asciichan.MainPage),
                  webapp2.Route(r'/unit3/blog', handler=blog.Posts),
                  webapp2.Route(r'/unit3/blog/newpost', handler=blog.NewPost),
                  webapp2.Route(r'/unit3/blog/<post_id:\d+>', handler=blog.Post, name='post'),
                  webapp2.Route(r'/unit4/play', handler=play.MainPage),
                               ], debug=True)
