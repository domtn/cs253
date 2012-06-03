import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom
from string import letters

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

def parse_coords(coords_str):
  if coords_str:
    coords = coords_str.split(",")
    if len(coords) == 2:
      return (coords[1], coords[0])

def get_coords_from_xml(xml):
  x = minidom.parseString(xml)
  try:
    coords_str = x.getElementsByTagName("gml:coordinates")[0].childNodes[0].nodeValue
    return coords_str
  except Exception:
    return None

IP_URL="http://api.hostip.info/?ip="
def get_coords(ip):
  ip = '4.2.2.2'
  ip = '23.24.209.141'
  url = IP_URL + ip
  content = None
  try:
    content = urllib2.urlopen(url).read()
  except URLError:
    return

  if content:
    coords = parse_coords(get_coords_from_xml(content))
    if coords:
      lat, lon = coords
      return db.GeoPt(lat,lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
    markers = []
    for point in points:
      markers.append(''.join(["markers=",str(point.lat),",",str(point.lon)]))
    return GMAPS_URL + '&'.join(markers)

class Art(db.Model):
  title = db.StringProperty(required = True)
  art = db.TextProperty(required = True)
  coords = db.GeoPtProperty()
  created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
  def render_front(self, title="", art="", error=""):
    arts = db.GqlQuery("SELECT * FROM Art \
                     ORDER BY created DESC")

    # prevent the running of multiple queries
    arts = list(arts)

    # points = filter(None, (a.coords for a in arts))
    # find which arts have coords
    points = []
    arts_with_coords = []
    for a in arts:
      if a.coords:
        points.append(a.coords)
        a.img_url = gmaps_img([a.coords])
        arts_with_coords.append(a)
  
    # if we have any arts coords, make an image url
    all_img_urls = None
    if points:
      all_img_urls = gmaps_img(points)

    self.render("asciichan2.html", title=title, art=art, arts=arts, error=error, all_img_urls = all_img_urls)

  def get(self):
    #self.write(repr(self.request.remote_addr))
    #self.write(repr(get_coords(self.request.remote_addr)))
    self.render_front()

  def post(self):
    title = self.request.get("title")
    art = self.request.get("art")

    if title and art:
      
      coords = get_coords(self.request.remote_addr)
      a = Art(title=title, art=art, coords=coords)

      a.put()

      self.redirect("/unit5/asciichan2")
    else:
      error = "we need both a title and some artwork!"
      self.render_front(title, art, error)


