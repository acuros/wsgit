import urlparse
import json, bson

class Environ(object):
    def __init__(self, request_dict):
        self.request_parameters = request_dict.get('parameters', {})
        self.meta = request_dict.get('meta', {})

    def get_dict(self):
        if hasattr(self, 'environ'):
            return self.environ
        environ = {}
        environ['REQUEST_METHOD'] = 'MOBILE'
        for key in ('REQUEST_URI', 'PATH_INFO', 'QUERY_STRING', 'REMOTE_ADDR', 'REMOTE_PORT'):
            environ[key] = getattr(self, '_get_%s'%key.lower())()
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

class WSGIHandler(object):
    def __init__(self):
        self.result = dict()

    def _start_response(self, status, response_headers):
        code, reason = status.split(' ')
        self.result['status'] = dict(code=code, reason=reason)

    def call_application(self, app, environ):
        app_iter = app(environ, self._start_response)
        try:
            for item in app_iter:
                self.result.update(json.loads(item))
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
        return bson.dumps(self.result)
