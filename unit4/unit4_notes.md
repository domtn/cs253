UNIT 4

Cookies

1. Cookie Domains:
   Set-Cookie: name=steve;Domain=www.reddit.com;Path=/foo

   Domain must have at minimum 2 periods. It specifies with domain a browser will send the cookie to

     Domains that will receive this cookie: (must end with www.reddit.com) 
       www.reddit.com
       foo.www.reddit.com
     Not receive cookie:
       reddit.com
       bar.reddit.com
    
   OTOH, browser will only accept cookies with "domain" param that are higher than the domain of the current server, for example:
    Say we're in www.reddit.com:
       www.reddit.com
       .reddit.com
    are ok. But you can't affect behaviors of other websites, such as:
       bar.reddit.com
       foo.reddit.com

2. Cookie Expiration:
   Set-Cookie: user=123; Expires: Tue, 1 Jan 2025 00:00:00 GMT

   "session" cookie = no expires

   N
Hashing

1. What is a hash?

   H(x) -> y
      x is data of any size 
      y is fixed-length bit string
         32-256 bit depending on algorithm used

2. Properties of a hash function?
   a. Difficult to generate a specific y
   b. Infeasible to find x for a given y. Ideally a one-way function
   c. Can't modify x without modifying y. E.g. Changing x a little bit and get completely different y.


3. Don't write your own hashing algorithm!

4. Popular hashing algos: (order of fast to slow, least to most secure)
   a. crc32 - checksums, fast, not secure, easy to find collision.
      Collision: two things hash to the same value  
   b. md5  - fast-ish, secure (NOT!)
      Can try making x longer and longer to induce a collision in MD5.
      It's okay if you limit length of x
   c. sha1 - secure-ish
   d. sha256 - pretty good 

