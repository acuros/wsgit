class AbstractRequest(object):
    TYPE_DETERMINER = None

    def __init__(self, handler, request_dict):
        if not isinstance(request_dict, dict):
            raise TypeError(
                'request_dict must be dict not %s' % type(request_dict)
            )

        self.handler = handler
        self.request_dict = request_dict
        self.headers = dict(
            ('HTTP_'+key.upper().replace('-', '_'), value)
            for key, value in self.request_dict.pop('headers', dict()).items()
        )
        self.url = request_dict.pop('url')
        self.params = request_dict.copy()

    @property
    def type(self):
        return self.__class__.__name__.replace('Request', '_request').lower()

    @classmethod
    def create(cls, handler, request_dict):
        if not isinstance(request_dict, dict):
            return InvalidRequest(handler, request_dict)
        determiners = dict(
            (RequestType.TYPE_DETERMINER, RequestType)
            for RequestType in cls.__subclasses__()
            if RequestType.TYPE_DETERMINER
        )
        request_class = determiners.get(request_dict.get('url', '\x00')[0])
        if not request_class:
            request_class = InvalidRequest
        return request_class(handler, request_dict)


class WebRequest(AbstractRequest):
    TYPE_DETERMINER = '/'

    def __init__(self, handler, request_dict):
        super(WebRequest, self).__init__(handler, request_dict)
        self.request_method = request_dict.pop('method', None)

    @property
    def is_valid(self):
        if self.request_method is None:
            return False
        return True


class CommandRequest(AbstractRequest):
    TYPE_DETERMINER = ':'

    def __init__(self, handler, request_dict):
        super(CommandRequest, self).__init__(handler, request_dict)
        self.command = getattr(self, 'do_'+self.url[1:], None)

    @property
    def is_valid(self):
        if self.command is None:
            return False
        return True

    def do_hello(self):
        return dict(status=dict(code='200', reason='OK'))


class InvalidRequest(AbstractRequest):

    def __init__(self, handler, request_dict):
        pass

    @property
    def is_valid(self):
        return False