import json
import re
import urlparse
import urllib
from StringIO import StringIO
from wsgit.request import WebRequest


class Environ(object):

    def __init__(self, request, meta):
        if not isinstance(request, WebRequest):
            raise TypeError('request must be an instance of WebRequest')

        if not isinstance(meta, dict):
            raise TypeError('meta must be an instance of dict')

        self.request = request
        self.meta = meta.copy()

    def get_dict(self):
        if hasattr(self, '_environ'):
            return self._environ
        environ = dict()
        for key in (
            'REQUEST_URI', 'PATH_INFO', 'QUERY_STRING', 'REMOTE_ADDR',
            'REMOTE_PORT', 'SERVER_NAME', 'SERVER_PORT', 'REQUEST_METHOD'
        ):
            environ[key] = getattr(self, '_get_%s' % key.lower())()
        environ.update(self._headers_for_environ())
        environ.update(self._get_wsgi_io_dict())
        self.environ = environ
        return environ

    def _get_request_method(self):
        return self.request.request_method

    def _get_request_uri(self):
        return self.request.url

    def _get_path_info(self):
        url = self.request.url
        if url is not None:
            return urlparse.urlparse(url).path

    def _get_query_string(self):
        url = self.request.url
        if url is not None:
            query = urlparse.urlparse(url).query
            return query

    def _get_remote_addr(self):
        return self.meta.get('remote_addr')

    def _get_remote_port(self):
        return self.meta.get('remote_port')

    def _get_server_name(self):
        return self.meta.get('server_name')

    def _get_server_port(self):
        return self.meta.get('server_port')

    def _get_wsgi_io_dict(self):
        post_body = urllib.urlencode(self.request.params)
        stream = StringIO()
        stream.write(post_body)
        stream.seek(0)
        return {
            'wsgi.input': stream,
            'wsgi.errors': StringIO(),
            'wsgi.version': (1, 0)
        }

    def _headers_for_environ(self):
        return dict(
            ('HTTP_'+key.upper().replace('-', '_'), value)
            for key, value in self.request.headers.items()
        )


class WSGIHandler(object):

    def __init__(self):
        self.result = dict(response=dict())

    def _start_response(self, status, response_headers):
        code, reason = status.split(' ')[0], ' '.join(status.split(' ')[1:])
        self.make_cookie(response_headers)
        self.result['status'] = dict(code=code, reason=reason)

    def call_application(self, app, environ):
        app_iter = app(environ, self._start_response)
        try:
            for item in app_iter:
                self._update_result(item)
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
        return self.result

    def _update_result(self, item):
        try:
            response = json.loads(item)
        except ValueError:
            self.result['no_json_response'] = \
                self.result.get('no_json_response', '') + item
        else:
            self.result['response'].update(response)

    def make_cookie(self, headers):
        raw_cookies = [value for key, value in headers if key.lower() == 'set-cookie']
        cookies = []
        for cookie in raw_cookies:
            matched = re.match(r'(\w+)=(?:"(.*?)(?<!\")|(.*?));', cookie)
            cookies.append(matched.group(0))
        self.cookies = cookies
