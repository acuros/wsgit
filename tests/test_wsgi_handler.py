import bson
import unittest
from wsgit.request import WebRequest
from wsgit.server import WSGITRequestHandler
from wsgit.wsgi import WSGIHandler, Environ
from applications import various_status_application,\
    no_json_response_application


class TestWSGIHandler(unittest.TestCase):

    def test_call_application(self):
        request = WebRequest(dict(url='/'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        bson_binary = handler.call_application(
            various_status_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(status=dict(reason='OK', code='200')),
            bson.loads(bson_binary)
        )

    def test_not_found_status(self):
        request = WebRequest(dict(url='/?404 NOT FOUND'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        bson_binary = handler.call_application(
            various_status_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(status=dict(reason='NOT FOUND', code='404')),
            bson.loads(bson_binary)
        )

    def test_no_json_response(self):
        request = WebRequest(dict(url='/?404 NOT FOUND'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        bson_binary = handler.call_application(
            no_json_response_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(
                status=dict(reason='NOT FOUND', code='404'),
                no_json_response='Page Not Found'
            ),
            bson.loads(bson_binary)
        )


class MockServer(object):
    _keyfile = None
    connected_handlers = []

    @staticmethod
    def app(*args):
        yield '{}'


class MockRequest(object):
    def __init__(self, request_bytes):
        self.request_bytes = request_bytes

    def getsockname(self):
        return '127.0.0.1'

    def recvobj(self):
        self.recvobj = lambda: None
        return bson.loads(self.request_bytes)

    def send(self, obj):
        pass

    def close(self):
        pass