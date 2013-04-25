import threading
import logging
from urlparse import urlparse, parse_qs
from SocketServer import BaseRequestHandler

from django.conf import settings
from django.core import urlresolvers

from imdjango.exceptions import IMError, NoParameterError, BadRequestError

logger = logging.getLogger('imdjango')

class IMRequestHandler(BaseRequestHandler):
    def setup(self):
        self.connection = self.request
        self.server.connected_handlers.append(self)

    def handle(self):
        while True:
            try:
                obj = self.connection.recvobj()
            except Exception:
                logger.debug('Bad Request. Not bson protocol.')
            if obj == None:
                break
            request = IMRequest(self, obj)
            self.start_view(request)

    def finish(self):
        self.connection.close()

    def start_view(self, request):
        thread = threading.Thread(target=self.reply_response, args=[request])
        thread.start()

    def reply_response(self, request):
        view, args, kwargs = self.get_resolver_match(request)
        try:
            response = view(request, *args, **kwargs)
        except IMError, e:
            logger.info('Request : %s\n%s: %s\n\n'%(request, e.__class__.__name__, str(e)))
            self.connection.sendobj({'status':{'code':e.__class__.__name__, 'reason':str(e)}})
            response = dict(status=dict(code=e.__class__.__name__, reason=str(e)))
        else:
            response.update(dict(status=dict(code='OK', reason='OK')))
        self.connection.sendobj(response)

    def get_resolver_match(self, request):
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        MOBILE_URL_PREFIX = getattr(settings, 'MOBILE_URL_PREFIX', '^/')
        resolver = urlresolvers.RegexURLResolver(MOBILE_URL_PREFIX, urlconf)
        return resolver.resolve(request.META['PATH_INFO'])
    


class IMRequest:
    def __init__(self, handler, obj):
        self.obj = obj
        self.META = dict(REQUEST_METHOD = "MOBILE",
                         PATH_INFO = self.get_parsed_url().path,
                         QUERY_STRING = self.get_parsed_url().query,
                         REMOTE_ADDR = handler.client_address[0]
                         )
        self.GET = self.get_GET()
        self.POST = self.get_POST()

    def get_GET(self):
        parsed_qs = parse_qs(self.get_parsed_url().query)
        for key, value in parsed_qs.copy().iteritems():
            if len(value) == 1:
                parsed_qs[key] = value[0]
        return parsed_qs

    def get_POST(self):
        parameters = self.obj.copy()
        del parameters['url']
        return parameters

    def get_url(self):
        try:
            return self.obj['url']
        except KeyError:
            raise NoParameterError('url')

    def get_parsed_url(self):
        if hasattr(self, '_parsed_url'):
            return self._parsed_url
        try:
            self._parsed_url = urlparse(self.get_url())
            return self._parsed_url
        except Exception:
            raise BadRequestError('Bad URL')
