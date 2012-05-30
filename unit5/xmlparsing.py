import urllib2
from xml.dom import minidom

#x = minidom.parseString("<mytag>contents!<children><item>1</item></children></mytag")
#x.toprettyxml()
#x.getElementsByTagName("item")[0].childNodes[0].nodeValue

def fetchDoc(url):
    p = urllib2.urlopen(url)
    return p.read()

def countTagOccurences(doc, tag):
    x = minidom.parseString(doc)
    return len(x.getElementsByTagName(tag))


url = "http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml"
print countTagOccurences(fetchDoc(url), "item")