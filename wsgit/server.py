#!/usr/bin/python
from gevent import monkey
monkey.patch_all()


def patch_bson_socket():
    from gevent.socket import socket
    from bson import network
    socket.recvbytes = network._recvbytes
    socket.recvobj = network._recvobj
    socket.sendobj = network._sendobj
patch_bson_socket()

from gevent.server import StreamServer
from wsgi import WSGIHandler, Environ
from wsgit.request import AbstractRequest, InvalidRequest


class Server(StreamServer):
    def __init__(self, listener, app, keyfile=None, certfile=None):
        self.app = app
        self.keyfile = keyfile
        self.certfile = certfile

        if keyfile and certfile:
            StreamServer.__init__(
                self,
                listener,
                self.handle,
                keyfile=keyfile,
                certfile=certfile
            )
        else:
            StreamServer.__init__(self, listener, self.handle)

    def handle(self, sock, addr):
        handler = WSGITRequestHandler(self, sock, addr)
        handler.handle()
        handler.finish()

    @staticmethod
    def run_server(*args, **kwargs):
        import threading
        server = Server(*args, **kwargs)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        return server


class WSGITRequestHandler(object):
    meta = dict()
    is_connected = True

    def __init__(self, server, conn, client_address):
        self.server = server
        self.conn = conn
        self.client_address = client_address
        self.meta = dict(
            server_name=self.conn.getsockname()[0],
            server_port=self.conn.getsockname()[1],
            remote_addr=self.client_address[0],
            remote_port=self.client_address[1]
        )
        self.headers = dict()
        self.allow_headers = []

    def handle(self):
        while self.is_connected:
            request = self._get_request()
            obj = getattr(self, 'deal_with_' + request.type,
                    'deal_with_unknown_request')(request)
            if request.is_valid:
                obj['url'] = request.url
                print obj
                self.conn.sendobj(obj)

    def _get_request(self):
        try:
            request_dict = self.conn.recvobj()
        except ValueError:
            request_dict = dict()
        request = AbstractRequest.create(self, request_dict)
        return request

    def deal_with_web_request(self, request):
        if not request.is_valid:
            return dict(status=dict(code='400', reason='BadRequest'))
        environ = Environ(request, self.meta)
        wsgi_handler = WSGIHandler()
        obj = wsgi_handler.call_application(self.server.app,
                                            environ.get_dict())

        obj['headers'] = dict(
            (key, value)
            for key, value in wsgi_handler.headers.iteritems()
            if key.lower() in self.allow_headers
        )
        obj['method'] = request.request_method
        return obj

    def deal_with_command_request(self, request):
        response = request.command()
        return response

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
    import os
    import sys
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
        app = getattr(module, name)
        server = Server.run_server((ip, int(port)), app)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    run()
