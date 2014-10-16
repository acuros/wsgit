Changelog
_________
* 2014.10.17: **0.3.1**:

    * Install requires gevent

* 2014.10.15: **0.3.0**:

    * Send HTTP Signature - Url, Method
    * Command Request "allow-headers", "set-headers" added
    * Do not pass headers from server in default
    * Print response log, currently it cannot be offed

* 2014.09.24: **0.2.2**:

    * REMOTE_ADDR bug fixed

* 2014.09.18: **0.2.1**:

    * Under gevent
    * You must put "method" parameter to choose method
    * CommandRequest added, some features will be implemented

* 2014.09.14: **0.1.3**:

    * Supports HTTP Request headers


* 2013.10.05: **0.1.2**:

    * Command ``wsgit`` supports ssl options ``--keyfile`` and ``--certfile``

* 2013.10.03: **0.1.1**:

    * Supports SSL

* 2013.09.22: **0.1**:

    * create mock environ to call wsgi application
    * run server with command ``wsgit``
