import webapp2
from unit1 import dateform
from unit2 import rot13
from unit2 import signup
from unit3 import asciichan
from unit3 import blog
from unit4 import play
from unit4 import authen
from unit5 import asciichan2
from unit5 import blog_api
from unit5 import blog_authen
from bloggy import bloggy
from unit6 import asciichan3

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
                  webapp2.Route(r'/unit3/blog/<post_id:\d+>', handler=blog.Post),
                  webapp2.Route(r'/unit4/play', handler=play.MainPage),
                  webapp2.Route(r'/unit4/authen/signup', handler=authen.SignupPage),
                  webapp2.Route(r'/unit4/authen/login', handler=authen.LoginPage),
                  webapp2.Route(r'/unit4/authen/logout', handler=authen.LogoutPage),
                  webapp2.Route(r'/unit4/authen/welcome', handler=authen.WelcomePage),
                  webapp2.Route(r'/unit5/asciichan2', handler=asciichan2.MainPage),
                  webapp2.Route(r'/unit5/blog<format:(?:/.json)?>', handler=blog_api.Posts),
                  webapp2.Route(r'/unit5/blog/newpost', handler=blog_api.NewPost),
                  webapp2.Route(r'/unit5/blog/<post_id:\d+><format:(?:.json)?>', handler=blog_api.Post),
                  webapp2.Route(r'/unit5/blog/signup', handler=blog_authen.SignupPage),
                  webapp2.Route(r'/unit5/blog/login', handler=blog_authen.LoginPage),
                  webapp2.Route(r'/unit5/blog/logout', handler=blog_authen.LogoutPage),
                  webapp2.Route(r'/unit5/blog/welcome', handler=blog_authen.WelcomePage),
                  webapp2.Route(r'/unit6/asciichan3', handler=asciichan3.MainPage),
                  webapp2.Route(r'/bloggy/blog<format:(?:/.json)?>', handler=bloggy.Posts),
                  webapp2.Route(r'/bloggy/blog/newpost', handler=bloggy.NewPost),
                  webapp2.Route(r'/bloggy/blog/<post_id:\d+><format:(?:.json)?>', handler=bloggy.Post),
                  webapp2.Route(r'/bloggy/signup', handler=bloggy.SignupPage),
                  webapp2.Route(r'/bloggy/login', handler=bloggy.LoginPage),
                  webapp2.Route(r'/bloggy/logout', handler=bloggy.LogoutPage),
                               ], debug=True)
