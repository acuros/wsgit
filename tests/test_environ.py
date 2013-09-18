#-*-coding:utf8-*-
'''Tests for Environ object'''

import unittest
from wsgit.request import Environ

def environ(request_parameters, meta={}):
    return Environ({'parameters':request_parameters, 'meta':meta}).get_dict()

class TestEnviron(unittest.TestCase):
    def test_request_method(self):
        self.assertEqual(environ({})['REQUEST_METHOD'], 'MOBILE')

    def test_reqeust_uri(self):
        self.assertEqual(environ({})['REQUEST_URI'], None)
        self.assertEqual(environ({'uri':'/'})['REQUEST_URI'], '/')
        self.assertEqual(environ({'uri':'/foo/bar/'})['REQUEST_URI'],
                                 '/foo/bar/')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'}['REQUEST_URI'], 
                                 '/foo/bar/?foo=bar'))

    def test_path_info(self):
        self.assertEqual(environ({}).get('PATH_INFO'), None)
        self.assertEqual(environ({'url':'/'})['PATH_INFO'], '/')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'})['PATH_INFO'], 
                                 '/foo/bar/')
        self.assertEqual(environ({'url':'/foo//'})['PATH_INFO'], '/foo/')

    def test_query_string(self):
        self.assertEqual(environ({}).get('QUERY_STRING'), None)
        self.assertEqual(environ({'url':'/'}).get('QUERY_STRING'), '')
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'})['PATH_INFO'], 
                                 'foo=bar')
        self.assertEqual(environ({'url': '/?foo=bar&foo2=bar2'})['PATH_INFO'], 
                                 'foo=bar&foo2=bar2')

    def test_remote_addr(self):
        self.assertEqual(Environ({}).get_dict().get('REMOTE_ADDR'), None)
        self.assertEqual(environ(meta={'ip':'127.0.0.1'})['REMOTE_ADDR'],
                                 '127.0.0.1')

    def test_remote_port(self):
        self.assertEqual(Environ({}).get_dict().get('REMOTE_PORT'), None)
        self.assertEqual(environ(meta={'port':10295})['REMOTE_PORT'], '10295')
