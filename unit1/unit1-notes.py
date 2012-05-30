UNIT 1

Inline vs Block element:
   text <br> text: inline element, so is <img>
   <p>text</p> text: block element, creates invisible box around element


Fragments:
   http://www.example.com/path#fragment


HTTP Request:
   
   URL: http://www.example.com/foo
   
   Request line:

    GET /foo HTTP/1.1
      "GET": method, Get or Post
      "/foo": path
      "HTTP/1.1": version (1.1 or 1.0)

    Headers:
       Syntax is "Name-w-hyphens: Value"

       Host: www.example.com 
       User-Agent: chrome v.17

       Valid headers:
         Host: www.hipmunk.com
         User-Agent: ignor me I'm a spammer
         i-made-this-up: whatever
       
       Invalid headers:
         User Agent: Chrome
         host www.example.com

HTTP Response:

    Status line:

    HTTP/1.1 200 OK
      "200": status code
            200 - OK
            302 - Found
            404 - Not Found
            500 - Server Error

      "OK": reason phrase

    Headers:
      Date: Tue Mar 2012 04:33:33 GMT
      Server: Apache/2.2.3
      Content-Type: text/html;
      Content-Length: 1539

      Should camourflage "Server" to something else to prevent exposing stack to would-be hacker


Telnet:
    
    $ telnet www.udacity.com 80
    >> GET / HTTP/1.0
    
    Why 1.0 and not 1.1 ? Default behavior of 1.1 is to keep the connection open for browsers to make subsequent requests. This is not convenient for Telnet.


    