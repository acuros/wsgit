import bson
import unittest
from mocks import MockHandler
from wsgit.request import AbstractRequest
from wsgit.wsgi import WSGIHandler, Environ
from applications import various_status_application,\
    no_json_response_application


class TestWSGIHandler(unittest.TestCase):

    def test_call_application(self):
        request = AbstractRequest.create(MockHandler(), dict(url='/'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        json_response = handler.call_application(
            various_status_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(status=dict(reason='OK', code='200'), response=dict()),
            json_response
        )

    def test_not_found_status(self):
        request = AbstractRequest.create(MockHandler(), dict(url='/?404 NOT FOUND'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        json_response = handler.call_application(
            various_status_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(status=dict(reason='NOT FOUND', code='404'), response=dict()),
            json_response
        )

    def test_no_json_response(self):
        request = AbstractRequest.create(MockHandler(), dict(url='/?404 NOT FOUND'))
        meta = dict(ip='127.0.0.1', port=19234)
        environ, handler = Environ(request, meta), WSGIHandler()
        json_response = handler.call_application(
            no_json_response_application,
            environ.get_dict()
        )
        self.assertEqual(
            dict(
                status=dict(reason='NOT FOUND', code='404'),
                no_json_response='Page Not Found', response=dict()
            ),
            json_response
        )