WSGIT (WSGI on TCP)
~~~~~~~~~~~~~~~~~~~

WSGIT is an adaptor which make WSGI applications run on ``TCP`` not HTTP.
It makes fake WSGI Request from TCP to run WSGI application.
It receives json response from WSGI application and sends it as bson after adds some HTTP header information in dict.
