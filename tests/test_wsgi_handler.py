import unittest
from wsgit.wsgi import WSGIHandler, Environ

def application(environ, start_response):
    import json
    start_response('200 OK', [('Content-Type', 'application/json')])
    yield '{}'

class TestWSGIHandler(unittest.TestCase):
    def test_call_application(self):
        request = dict(meta=dict(ip='127.0.0.1', port=19234), 
                       parameters=dict(url='/'))
        environ = Environ(request)
        handler = WSGIHandler()
        json_text = handler.call_application(application, environ.get_dict())
        self.assertEqual('{"status": {"reason": "OK", "code": "200"}}', json_text)

