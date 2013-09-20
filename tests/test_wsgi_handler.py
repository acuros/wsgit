import unittest
import bson
from wsgit.wsgi import WSGIHandler, Environ
from tests.applications import application1 as app

class TestWSGIHandler(unittest.TestCase):
    def test_call_application(self):
        request = dict(meta=dict(ip='127.0.0.1', port=19234), 
                       parameters=dict(url='/'))
        environ = Environ(request)
        handler = WSGIHandler()
        bson_binary = handler.call_application(app, environ.get_dict())
        self.assertEqual(dict(status=dict(reason='OK', code='200')),
                         bson.loads(bson_binary))
