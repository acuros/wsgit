class AbstractRequest(dict):
    TYPE_DETERMINER = None

    def __init__(self, request_dict, meta=None):
        if meta is None:
            meta = dict()
        if not isinstance(request_dict, dict):
            raise TypeError(
                'request_dict must be dict not %s' % type(request_dict)
            )
        if not isinstance(meta, dict):
            raise TypeError('meta must be dict not %s' % type(meta))

        self.request_dict = request_dict

    @property
    def type(self):
        return self.__class__.__name__.replace('Request', '_request').lower()

    @property
    def headers(self):
        return dict(
            ('HTTP_'+key.upper().replace('-', '_'), value)
            for key, value in self.request_dict.pop('__headers__',
                                                    dict()).items()
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


class CommandRequest(AbstractRequest):
    TYPE_DETERMINER = ':'


class InvalidRequest(AbstractRequest):
    def __init__(self, request_dict, meta=None):
        pass