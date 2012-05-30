import webapp2
from util import html_util
import rotation

form="""
<form method="post">
  <h3>Enter some text to ROT13:</h3>
    <textarea name="text" rows=10 cols=60>%(text)s</textarea>
  </label> 
  <br>
  <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
  def write_form(self, text=""):
    self.response.out.write(form % {"text": html_util.escape_html(rotation.rotate_13(text))})

  def get(self):
    self.write_form()

  def post(self):
    self.write_form(self.request.get('text'))