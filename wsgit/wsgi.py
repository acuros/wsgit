import urlparse
import urllib
from StringIO import StringIO
import json
import bson


class Environ(object):

    def __init__(self, request_dict):
        self.request_parameters = request_dict.get('parameters', {})
        self.meta = request_dict.get('meta', {})

    def get_dict(self):
        if hasattr(self, 'environ'):
            return self.environ
        environ = {}
        environ['REQUEST_METHOD'] = 'MOBILE'
        for key in ('REQUEST_URI', 'PATH_INFO', 'QUERY_STRING', 'REMOTE_ADDR',
                    'REMOTE_PORT', 'SERVER_NAME', 'SERVER_PORT'):
            environ[key] = getattr(self, '_get_%s' % key.lower())()
        environ.update(self._get_wsgi_io_dict())
        self.environ = environ
        return environ

    def _get_request_uri(self):
        return self.request_parameters.get('url')

    def _get_path_info(self):
        url = self.request_parameters.get('url')
        if url is not None:
            return urlparse.urlparse(url).path

    def _get_query_string(self):
        url = self.request_parameters.get('url')
        if url is not None:
            query = urlparse.urlparse(url).query
            return query

    def _get_remote_addr(self):
        return self.meta.get('ip')

    def _get_remote_port(self):
        return self.meta.get('port')

    def _get_server_name(self):
        return self.meta.get('server_name')

    def _get_server_port(self):
        return self.meta.get('server_port')

    def _get_wsgi_io_dict(self):
        parameters = self.request_parameters.copy()
        if 'url' in parameters:
            del parameters['url']
        post_body = urllib.urlencode(parameters)
        stream = StringIO()
        stream.write(post_body)
        stream.seek(0)
        return {'wsgi.input': stream, 'wsgi.errors': StringIO(),
                'wsgi.version': (1, 0)}


class WSGIHandler(object):

    def __init__(self):
        self.result = dict()

    def _start_response(self, status, response_headers):
        code, reason = status.split(' ')[0], ' '.join(status.split(' ')[1:])
        self.result['status'] = dict(code=code, reason=reason)

    def call_application(self, app, environ):
        app_iter = app(environ, self._start_response)
        try:
            for item in app_iter:
                self._update_result(item)
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
        return bson.dumps(self.result)

    def _update_result(self, item):
        try:
            response = json.loads(item)
        except ValueError:
            self.result['no_json_response'] = \
                self.result.get('no_json_response', '') + item
        else:
            self.result.update(response)
