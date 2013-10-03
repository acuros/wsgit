import unittest
import bson
from wsgit.wsgi import WSGIHandler, Environ
from tests.applications import various_status_application,\
    no_json_response_application


class TestWSGIHandler(unittest.TestCase):

    def test_call_application(self):
        request = dict(meta=dict(ip='127.0.0.1', port=19234),
                       parameters=dict(url='/'))
        environ, handler = Environ(request), WSGIHandler()
        bson_binary = handler.call_application(various_status_application,
                                               environ.get_dict())
        self.assertEqual(dict(status=dict(reason='OK', code='200')),
                         bson.loads(bson_binary))

    def test_not_found_status(self):
        request = dict(meta=dict(ip='127.0.0.1', port=19234),
                       parameters=dict(url='/?404 NOT FOUND'))
        environ, handler = Environ(request), WSGIHandler()
        bson_binary = handler.call_application(various_status_application,
                                               environ.get_dict())
        self.assertEqual(dict(status=dict(reason='NOT FOUND', code='404')),
                         bson.loads(bson_binary))

    def test_no_json_response(self):
        request = dict(meta=dict(ip='127.0.0.1', port=19234),
                       parameters=dict(url='/?404 NOT FOUND'))
        environ, handler = Environ(request), WSGIHandler()
        bson_binary = handler.call_application(no_json_response_application,
                                               environ.get_dict())
        self.assertEqual(dict(status=dict(reason='NOT FOUND', code='404'),
                              no_json_response='Page Not Found'),
                         bson.loads(bson_binary)
                         )
