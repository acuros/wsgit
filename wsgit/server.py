#!/usr/bin/python
import bson
import ssl
import threading
from SocketServer import ThreadingMixIn, TCPServer, BaseRequestHandler

from wsgi import WSGIHandler, Environ


class Server(ThreadingMixIn, TCPServer):

    def __init__(self, addr, handler, app, ssl=False):
        self.app = app
        self.connected_handlers = []
        self._use_ssl = ssl
        TCPServer.__init__(self, addr, handler)

    @classmethod
    def run_server(cls, addr, app, ssl=False):
        bson.patch_socket()
        server = cls(addr, WSGITRequestHandler, app, ssl)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        return server, thread


class WSGITRequestHandler(BaseRequestHandler):
    meta = dict()

    def setup(self):
        if self.server._use_ssl:
            self.request = ssl.wrap_socket(self.request,
                                           keyfile='ssl.key',
                                           certfile='ssl.crt',
                                           server_side=True,
                                           ssl_version=ssl.PROTOCOL_TLSv1)
        self.conn = self.request
        self.server.connected_handlers.append(self)
        self.meta = dict()

    def handle(self):
        while True:
            try:
                obj = self.conn.recvobj()
            except Exception:
                logger.debug('Bad Request. Not bson protocol.')
            if obj is None:
                break
            environ = self._get_environ(obj)
            wsgi_handler = WSGIHandler()
            obj = wsgi_handler.call_application(self.server.app,
                                                environ.get_dict())
            self.conn.send(obj)

    def _get_environ(self, parameters):
        if '__headers__' in parameters and \
                isinstance(parameters['__headers__'], dict):
            headers = dict(
                ('HTTP_'+key.upper(), value)
                for key, value in parameters.pop('__headers__').items()
            )
            self.meta.update(headers)
        return Environ(dict(meta=self.meta, parameters=parameters))

    def finish(self):
        self.conn.close()


def run():
    import sys
    import os
    import time
    sys.path.append(os.getcwd())
    if len(sys.argv) != 3:
        print 'Usage : %s ipaddr:port module.application' % sys.argv[0]
        sys.exit(1)
    path = sys.argv[2].split('.')
    name = path[-1]
    module = __import__('.'.join(path[:-1]), fromlist=[name])
    ip, port = sys.argv[1].split(':')
    try:
        server, thread = Server.run_server(
            (ip, int(port)), getattr(module, name))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == '__main__':
    run()
