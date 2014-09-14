class AbstractRequest(dict):
    TYPE_DETERMINER = None

    def __init__(self, request_dict):
        if not isinstance(request_dict, dict):
            raise TypeError(
                'request_dict must be dict not %s' % type(request_dict)
            )

        self.request_dict = request_dict

    @property
    def type(self):
        return self.__class__.__name__.replace('Request', '_request').lower()

    @property
    def headers(self):
        return dict(
            ('HTTP_'+key.upper().replace('-', '_'), value)
            for key, value in self.request_dict.pop('headers', dict()).items()
        )

    @classmethod
    def create(cls, request_dict):
        if not isinstance(request_dict, dict):
            return InvalidRequest(request_dict)
        determiners = dict(
            (RequestType.TYPE_DETERMINER, RequestType)
            for RequestType in cls.__subclasses__()
            if RequestType.TYPE_DETERMINER
        )
        request_class = determiners.get(request_dict.get('url', '\x00')[0])
        if not request_class:
            request_class = InvalidRequest
        return request_class(request_dict)


class WebRequest(AbstractRequest):
    TYPE_DETERMINER = '/'

    def __init__(self, request_dict):
        super(WebRequest, self).__init__(request_dict)


class CommandRequest(AbstractRequest):
    TYPE_DETERMINER = ':'

    def __init__(self, request_dict):
        super(CommandRequest, self).__init__(request_dict)


class InvalidRequest(AbstractRequest):
    def __init__(self, request_dict):
        pass