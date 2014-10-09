import unittest
from mocks import MockHandler
from applications import various_status_application
from wsgit.request import AbstractRequest, WebRequest, CommandRequest, \
    InvalidRequest
from wsgit.wsgi import Environ, WSGIHandler


class TestRequest(unittest.TestCase):
    def test_invalid_request(self):
        request = AbstractRequest.create(MockHandler(), dict(url='\x00'))
        self.assertIsInstance(request, InvalidRequest)


class TestCommandRequest(unittest.TestCase):
    def test_create(self):
        request = AbstractRequest.create(MockHandler(), dict(url=':init'))
        self.assertIsInstance(request, CommandRequest)

    def test_command_hello(self):
        request = AbstractRequest.create(MockHandler(), dict(url=':hello'))
        self.assertEqual(
            request.command(),
            dict(status=dict(code='200', reason='OK'))
        )

    def test_command_set_headers(self):
        request = AbstractRequest.create(
            MockHandler(),
            dict(url=':set-headers', headers=dict(foo='bar'))
        )
        self.assertEqual(
            request.command(),
            dict(status=dict(code='200', reason='OK'), headers=dict(foo='bar'))
        )

    def test_command_allow_headers(self):
        def get_application_response(request_handler):
            request = AbstractRequest.create(request_handler, dict(url='/'))
            meta = dict(ip='127.0.0.1', port=19234)
            environ = Environ(request, meta)
            wsgi_handler = WSGIHandler(request_handler)
            return wsgi_handler.call_application(
                various_status_application,
                environ.get_dict()
            )

        request_handler = MockHandler()

        headers = get_application_response(request_handler)['headers']
        self.assertNotIn('Content-Type', headers)

        request = AbstractRequest.create(
            request_handler,
            dict(url=':allow-headers', names=['content-type'])
        )
        self.assertEqual(
            request.command(),
            dict(status=dict(code='200', reason='OK'))
        )
        self.assertIn('content-type', request_handler.allow_headers)

        headers = get_application_response(request_handler)['headers']
        self.assertIn('Content-Type', headers)


class TestWebRequest(unittest.TestCase):
    def test_create(self):
        request = AbstractRequest.create(MockHandler(), dict(url='/', foo='bar'))
        self.assertIsInstance(request, WebRequest)
        self.assertEqual(request.url, '/')
        self.assertEqual(request.params, dict(foo='bar'))

    def test_http_header(self):
        request = {'url': '/', 'headers': dict(USER_AGENT='iPhone')}
        request = AbstractRequest.create(MockHandler(), request)
        self.assertEqual(request.headers['USER_AGENT'], 'iPhone')
