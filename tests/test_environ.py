#-*-coding:utf8-*-
'''Tests for Environ object'''

import uniitest
from wsgit import Environ

def environ(request):
    return Environ(request).get_dict()

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
        self.assertEqual(environ({'url': '/foo/bar/?foo=bar'}['PATH_INFO'], 
                                 '/foo/bar/'))
