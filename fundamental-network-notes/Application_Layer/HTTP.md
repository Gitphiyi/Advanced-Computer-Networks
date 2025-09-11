# HTTP (Hypertext Transfer Protocol)
## What is HTTP?
- HTTP is a stateless Application Layer protocol usually built on top of TCP for communication between clients and servers
- Developed by CERN in 1989 to define a universal way of fetching and linking documents over the Internet. It was designed to be simple enough to be implemented on any machine, work on any platform (Linux, Window, Unix, etc), allow extra features (headers for authentication, cookies, etc.), and support HTML documents linking to other resources (images, text, scripts, etc.)
- A key point about HTTP is that it is stateless, meaning every request and response are independent of each other. 
- HTTP Request consists of: HTTP version type, URL, method, headers, optional body, etc.
- HTTP Response consists of: HTTP version type, Status Code, headers, body, etc.

## Basic Protocol
1. Client sets up TCP handshake with server
2. Client sends GET/POST/PUSH request to server and server can respond with HTTP Response
3. 

Session tracking = Identify multiple HTTP requests as all coming from the same client
Cookies are used to track sessions i.e. identify sequences of related browser requests. After receiving cookie, browser includes it in HTTP headers of all subsequent requests to the same domain. Cookies often used in authentication. Cookies usually placed in browser memory
If a browser receives a cookie it will use that cookie in every subsequent request’s header to the same domain

## HTTPS
- HTTPS is a secure HTTP protocol 
- It essentially is the HTTP protocol where the TCP protocol underneath is wrapped with TLS security

## Evolution of HTTP
### HTTP 1.0
### HTTP 1.1
### HTTP 2.0
### HTTP 3.0