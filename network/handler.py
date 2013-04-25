import bson, threading, logging
from urlparse import urlparse, parse_qs
from SocketServer import BaseRequestHandler

from django.conf import settings
from django.core import urlresolvers

from imdjango.exceptions import *

logger = logging.getLogger('imdjango')

class IMRequestHandler(BaseRequestHandler):
    def setup(self):
        self.connection = self.request
        self.server.connected_handlers.append(self)

    def handle(self):
        while True:
            try:
                obj = self.connection.recvobj()
            except Exception, e:
                logger.error('Bad Request. Not bson protocol.')
            if obj == None:
                break
            request = IMRequest(obj)
            thread = threading.Thread(target=self.reply_response, args=[request]).start()

    def finish(self):
        self.connection.close()

    def reply_response(self, request):
        view, args, kwargs = self.get_resolver_match(request)
        response = view(request, *args, **kwargs)
        self.connection.sendobj(response)

    def get_resolver_match(self, request):
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
        return resolver.resolve(request.META['PATH_INFO'])
    


class IMRequest:
    def __init__(self, obj):
        self.obj = obj
        parsed_url = self.get_parsed_url()
        self.META = dict(
                            PATH_INFO = parsed_url.path,
                            QUERY_STRING = parsed_url.query
                        )
        self.GET = parse_qs(parsed_url.query)

    def get_url(self):
        try:
            return self.obj['url']
        except KeyError:
            raise NoParameterError('url')

    def get_parsed_url(self):
        try:
            return urlparse(self.get_url())
        except Exception:
            raise BadRequestError('Bad URL')
