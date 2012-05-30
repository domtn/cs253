import webapp2
from unit1 import dateform
from unit2 import rot13
from unit2 import signup
from unit3 import asciichan
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

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/unit1/dateform', dateform.MainPage),
                               ('/unit1/thanks', dateform.ThanksPage), 
                               ('/unit2/rot13', rot13.MainPage),
                               ('/unit2/signup', signup.MainPage),
                               ('/unit2/welcome', signup.WelcomePage),
                               ('/unit3/asciichan', asciichan.MainPage),
                               ('/unit4/play', play.MainPage),
                               ], debug=True)