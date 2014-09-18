#-*-coding:utf8-*-
'''Tests for Environ object'''

import unittest
from wsgit.request import AbstractRequest
from wsgit.wsgi import Environ


def environ(request_parameters, meta=None):
    if not request_parameters:
        request_parameters = dict()
    if not meta:
        meta = dict()
    request = AbstractRequest.create(object(), request_parameters)
    return Environ(request, meta).get_dict()


class TestEnviron(unittest.TestCase):

    def test_request_method(self):
        request_dict = {'url': '/', 'method': 'GET'}
        self.assertEqual(environ(request_dict)['REQUEST_METHOD'], 'GET')
        env = environ({'url': '/', 'method': 'POST', 'foo': 'bar'})
        self.assertEqual(env['REQUEST_METHOD'], 'POST')

    def test_reqeust_uri(self):
        self.assertEqual(environ({'url': '/'})['REQUEST_URI'], '/')
        self.assertEqual(environ({'url': '/foo/bar/'})['REQUEST_URI'],
                         '/foo/bar/')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'})['REQUEST_URI'],
                         '/foo/bar/?foo=bar')

    def test_path_info(self):
        self.assertEqual(environ({'url': '/'})['PATH_INFO'], '/')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'})['PATH_INFO'],
                         '/foo/bar/')

    def test_query_string(self):
        self.assertEqual(environ({'url': '/'}).get('QUERY_STRING'), '')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'})['QUERY_STRING'],
                         'foo=bar')
        self.assertEqual(
            environ({'url': '/?foo=bar&foo2=bar2'})['QUERY_STRING'],
            'foo=bar&foo2=bar2')

    def test_remote_addr(self):
        env = environ({'url': '/'}, meta={'ip': '127.0.0.1'})
        self.assertEqual(env['REMOTE_ADDR'], '127.0.0.1')

    def test_remote_port(self):
        env = environ({'url': '/'}, meta={'port': 10295})
        self.assertEqual(env['REMOTE_PORT'], 10295)

    def test_server_name(self):
        env = environ({'url': '/'}, meta={'server_name': '10.20.30.40'})
        self.assertEqual(env['SERVER_NAME'], '10.20.30.40')

    def test_server_port(self):
        self.assertEqual(
            environ({'url': '/'}, meta={'server_port': 9338})['SERVER_PORT'],
            9338
        )

    def test_post_data(self):
        request_dict = {'url': '/', 'user_id': '13671', 'article_id': '5312'}
        env_dict = environ(request_dict)
        self.assertTrue('wsgi.input' in env_dict)
        from urlparse import parse_qs
        parsed_post = parse_qs(env_dict['wsgi.input'].read())
        self.assertEqual(parsed_post,
                         {'article_id': ['5312'], 'user_id': ['13671']})

    def test_http_headers(self):
        request_dict = {'url': '/', 'headers': {'Accept': 'application/json'}}
        env_dict = environ(request_dict)
        self.assertEquals(env_dict['HTTP_ACCEPT'], 'application/json')
