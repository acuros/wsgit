WSGIT (WSGI on TCP)
~~~~~~~~~~~~~~~~~~~

WSGIT is a server which runs WSGI applications on ``TCP`` not ``HTTP`` so that helps you make server of non-http-clients(such as mobile application) with wsgi applications(like django or flask).
It makes mock WSGI Request from TCP to run WSGI application.
It receives json response from WSGI application and sends it as bson after adds some HTTP header information in dict.

Django Example:

.. code-block:: python

    def index(request):
        return HttpResponse(json.dumps(dict(page='index')), mimetype='application/json')
    
    urlpatterns = patterns('',
        url(r'^$', index),
    )

Run Example:

.. code-block:: console

    $ python wsgit 0:9338 djangoproject.wsgi.application

Request Example:

.. code-block:: python

    >>> from socket import *
    >>> import bson
    >>> bson.patch_socket()
    >>> s = socket(AF_INET, SOCK_STREAM)
    >>> s.connect(('127.0.0.1', 9338))
    >>> s.sendobj({'url':'/'})
    >>> print s.recvobj()
    >>> {u'status': {u'reason': 'OK', u'code': '200'}, u'page': u'index'}
    >>> s.close()
