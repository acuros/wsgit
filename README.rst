WSGIT (WSGI on TCP)
~~~~~~~~~~~~~~~~~~~

WSGIT is an adaptor which make run WSGI applications on ``TCP`` not HTTP.
It makes fake WSGI Request from TCP to run WSGI application.
It receives json response from WSGI application and sends it after adds some HTTP header information in json.
