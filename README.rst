WSGIT (WSGI on TCP)
~~~~~~~~~~~~~~~~~~~


About
_____

WSGIT is a server which runs WSGI applications on ``TCP`` not ``HTTP`` so that helps you make server of non-http-clients(such as mobile application) with wsgi applications(like django or flask).
It makes mock WSGI Request from TCP to run WSGI application.
It receives json response from WSGI application and sends it as bson after adds some HTTP header information in dict.


Examples
________

Django Example:

.. code-block:: python

    def index(request):
        return HttpResponse(json.dumps(dict(page='index')), mimetype='application/json')
    
    urlpatterns = patterns('',
        url(r'^$', index),
    )

Run Example:

.. code-block:: console

    $ wsgit 0:9338 djangoproject.wsgi.application

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


Changelog
_________

* 2014.09.14: **0.1.3**:

    * Supports HTTP Request headers


* 2013.10.05: **0.1.2**:

    * Command ``wsgit`` supports ssl options ``--keyfile`` and ``--certfile``

* 2013.10.03: **0.1.1**:

    * Supports SSL

* 2013.09.22: **0.1**:

    * create mock environ to call wsgi application
    * run server with command ``wsgit``
