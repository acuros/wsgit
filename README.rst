WSGIT (WSGI on TCP)
~~~

WSGIT is an adaptor which make run WSGI applications on ``TCP`` not HTTP.
It make fake WSGI Request from TCP to run WSGI application.
It receives json response from WSGI application and send it after add some HTTP header information in json.
