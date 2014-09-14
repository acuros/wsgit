import unittest
from wsgit.request import AbstractRequest, WebRequest, CommandRequest, InvalidRequest


class TestRequest(unittest.TestCase):
    def test_command_request(self):
        request = AbstractRequest.create(dict(url=':init'))
        self.assertIsInstance(request, CommandRequest)
        self.assertEqual(request.command, 'init')

    def test_web_request(self):
        request = AbstractRequest.create(dict(url='/', foo='bar'))
        self.assertIsInstance(request, WebRequest)
        self.assertEqual(request.url, '/')
        self.assertEqual(request.params, dict(foo='bar'))

    def test_invalid_request(self):
        self.test_command_request()
        request = AbstractRequest.create(dict(url='\x00'))
        self.assertIsInstance(request, InvalidRequest)