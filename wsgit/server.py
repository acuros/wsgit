#!/usr/bin/python
import traceback
import bson
import ssl
import threading
from SocketServer import ThreadingMixIn, TCPServer, BaseRequestHandler

from wsgi import WSGIHandler, Environ
from wsgit.request import AbstractRequest, InvalidRequest


class Server(ThreadingMixIn, TCPServer):

    def __init__(self, addr, handler, app, keyfile=None, certfile=None):
        self.app = app
        self.connected_handlers = []
        self._keyfile = keyfile
        self._certfile = certfile
        TCPServer.__init__(self, addr, handler)

    @classmethod
    def run_server(cls, addr, app, keyfile=None, certfile=None):
        bson.patch_socket()
        server = cls(addr, WSGITRequestHandler, app, keyfile, certfile)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        return server, thread


class WSGITRequestHandler(BaseRequestHandler):
    meta = dict()
    is_connected = True

    def setup(self):
        if self.server._keyfile:
            self.request = ssl.wrap_socket(self.request,
                                           keyfile=self.server._keyfile,
                                           certfile=self.server._certfile,
                                           server_side=True,
                                           ssl_version=ssl.PROTOCOL_TLSv1)
        self.conn = self.request
        self.server.connected_handlers.append(self)
        self.meta = dict(
            server_name=self.conn.getsockname()[0],
            server_port=self.conn.getsockname()[1],
            remote_addr=self.client_address[0],
            remote_port=self.client_address[1]
        )

    def handle(self):
        while self.is_connected:
            request = self._get_request()
            getattr(self, 'deal_with_' + request.type,
                    'deal_with_unknown_request')(request)

    def _get_request(self):
        try:
            request_dict = self.conn.recvobj()
        except ValueError:
            request_dict = dict()
        return AbstractRequest.create(request_dict)

    def deal_with_web_request(self, request):
        environ = Environ(request, self.meta)
        wsgi_handler = WSGIHandler()
        obj = wsgi_handler.call_application(self.server.app,
                                            environ.get_dict())
        self.conn.send(obj)

    def deal_with_command_request(self, request):
        raise NotImplementedError

    def deal_with_invalid_request(self, request):
        if isinstance(request, InvalidRequest):
            self.is_connected = False

    def deal_with_unknown_request(self, request):
        raise NotImplementedError('Handling method for type %s is not '
                                  'implemented' % type(request))

    def finish(self):
        self.conn.close()


def run():
    import argparse
    import sys
    import os
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', metavar='ADDR',
                        help='bind ip with port(ex: 0:9338)')
    parser.add_argument('app', metavar='APP',
                        help='application for run(ex: modulename.application)')
    parser.add_argument('--keyfile', metavar='FILE')
    parser.add_argument('--certfile', metavar='FILE')
    args = parser.parse_args()
    sys.path.append(os.getcwd())
    path = args.app.split('.')
    name = path[-1]
    module = __import__('.'.join(path[:-1]), fromlist=[name])
    ip, port = args.addr.split(':')
    if args.keyfile or args.certfile:
        if not args.keyfile:
            raise argparse.ArgumentError('--keyfile', '--keyfile omitted')
        if not args.certfile:
            raise argparse.ArgumentError('--certfile', '--certfile omitted')

    try:
        server, thread = Server.run_server((ip, int(port)),
                                           getattr(module, name),
                                           args.keyfile,
                                           args.certfile
                                           )
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == '__main__':
    run()
