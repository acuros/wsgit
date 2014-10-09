import unittest
from mocks import MockHandler
from wsgit.request import AbstractRequest, WebRequest, CommandRequest, \
    InvalidRequest


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
