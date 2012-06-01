import urllib
import urllib2



p = urllib2.urlopen("http://www.google.com")
#equivalent of: curl -I "http://www.google.com"

c = p.read()

dir(p)

p.headers.items()




How to be a good citizen on the Internet

- use a good user-agent
- rate-limite yourself, include a sleep so you pause a little bit before hitting somebody too hard
  
import time 

while more: 
  get_more()
  time.sleep(1)


Common protocols for speaking with APIs on the Internet

- SOAP (Microsoft) - unnecessarily complicated
- Protocolbuffer(google)
- Thrift (facebook)
- plain text, custom protocol - not recommended

Good habits
- Sending proper user-agents
- Rate-limiting yourself
- Using common protocols and data formats

Bad habits
- Writing custom protocols
- Using SOAP