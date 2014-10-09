import bson


class MockServer(object):
    _keyfile = None
    connected_handlers = []

    @staticmethod
    def app(*args):
        yield '{}'


class MockRequest(object):
    def __init__(self, request_bytes):
        self.request_bytes = request_bytes

    def getsockname(self):
        return '127.0.0.1'

    def recvobj(self):
        self.recvobj = lambda: None
        return bson.loads(self.request_bytes)

    def send(self, obj):
        pass

    def close(self):
        pass


class MockHandler(object):
    def __init__(self):
        self.headers = dict()
        self.allow_headers = []
