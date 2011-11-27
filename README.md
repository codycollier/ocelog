ocelog (experimental)
=====================

Ocelog is an http gateway to syslog.  Clients can make http post requests to the ocelog server and those requests will be authenticated, validated, and then written to syslog on the local host in standard syslog format.

The ocelog server is a wsgi compliant application (uses the bottle micro framework) and can be run by most any wsgi-compliant server.  The core modules make use of the python standard library syslog module to write messages to the syslog service on the local host.  

The service accepts posted data in the common x-www-form-urlencoded format.  In addition to a required log message and application name, requests may include a facility, priority, or source host.  If enabled, a simple mac token based on a shared secret can be required as well.

client post:

```
[somehost]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded"
"http://someserver:8888/log" -d"appname=testapp" -d"msg=some event occured"
```


syslog result:

```
May  8 17:58:53 someserver 192.168.50.24 testapp: some event occured
```



The API
-------

GET  /

* Accepts nothing
* Returns help document


POST /log

* Accepts an x-www-form-urlencoded post of data and writes it to syslog
    * required: "appname" - string - the name or identifier of the log source
    * required: "msg" - string - the message to be writter
    * optional: "hostname" - The fqdn, hostname, or ip of the source host.  The 
        client ip will be used if this is not provided.
    * optional: "facility" - A valid syslog facility to use when writing the log
    * optional: "priority" - A valid syslog priority to use when writing the log
* Returns a 201 on success and a 400 on failure
    * Adds a message to x-ocelog-error header upon failure



Examples
--------

Below are some examples of http client requests against the api.


A simple message post with minimum parameters

```
[host]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded" 
"http://localhost:8888/log" -d"appname=testapp" -d"msg=some event occured"
> POST /log HTTP/1.1
> User-Agent: curl/7.16.3 
> Host: localhost:8888
> Accept: */*
> Content-Type:application/x-www-form-urlencoded
> Content-Length: 38
> 
< HTTP/1.0 201 CREATED
< Date: Tue, 13 Apr 2010 05:32:35 GMT
< Server: WSGIServer/0.1 Python/2.6.4
< Content-Type: text/html
< Content-Length: 0
< 
```



A complex message with more custom parameters

```
[host]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded" 
"http://localhost:8888/log" -d"facility=local1" -d"priority=info" 
-d"hostname=servicehost1" -d"appname=testapp" -d"msg=some event occured"
> POST /log HTTP/1.1
> User-Agent: curl/7.16.3
> Host: localhost:8888
> Accept: */*
> Content-Type:application/x-www-form-urlencoded
> Content-Length: 90
> 
< HTTP/1.0 201 CREATED
< Date: Tue, 13 Apr 2010 05:34:38 GMT
< Server: WSGIServer/0.1 Python/2.6.4
< Content-Type: text/html
< Content-Length: 0
< 
```



A message with an invalid facility

```
[host]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded" 
"http://localhost:8888/log" -d"facility=no-such-facility" -d"appname=testapp" -d"msg=some event occured"
> POST /log HTTP/1.1
> User-Agent: curl/7.16.3
> Host: localhost:8888
> Accept: */*
> Content-Type:application/x-www-form-urlencoded
> Content-Length: 64
> 
< HTTP/1.0 400 BAD REQUEST
< Date: Tue, 13 Apr 2010 05:35:11 GMT
< Server: WSGIServer/0.1 Python/2.6.4
< Content-Type: text/html
< X-Ocelog-Error: Message included invalid facility
< Content-Length: 0
< 
```



A message sending a valid security token for authorization

```
[host]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded" 
"http://localhost:8888/log" -d"appname=testapp" -d"msg=the coffee pot volume is low" 
-H "x-token:7d187dda6fcdc56f33832fbbca740808"
> POST /log HTTP/1.1
> User-Agent: curl/7.16.3
> Host: localhost:8888
> Accept: */*
> Content-Type:application/x-www-form-urlencoded
> x-token:7d187dda6fcdc56f33832fbbca740808
> Content-Length: 48
> 
< HTTP/1.0 201 CREATED
< Date: Tue, 13 Apr 2010 05:37:57 GMT
< Server: WSGIServer/0.1 Python/2.6.4
< Content-Type: text/html
< Content-Length: 0
< 
```



A message sending an invalid security token for authorization

```
[host]$curl -v -X POST -H "Content-Type:application/x-www-form-urlencoded" 
"http://localhost:8888/log" -d"appname=testapp" -d"msg=the coffee pot volume is low" 
-H "x-token:bad token here 6f33832fbbca740808"
> POST /log HTTP/1.1
> User-Agent: curl/7.16.3
> Host: localhost:8888
> Accept: */*
> Content-Type:application/x-www-form-urlencoded
> x-token:bad token here 6f33832fbbca740808
> Content-Length: 48
> 
< HTTP/1.0 400 BAD REQUEST
< Date: Tue, 13 Apr 2010 05:38:17 GMT
< Server: WSGIServer/0.1 Python/2.6.4
< Content-Type: text/html
< X-Ocelog-Error: Request failed authorization
< Content-Length: 0
< 
```


