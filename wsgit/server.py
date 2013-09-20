import threading
import bson
from SocketServer import ThreadingMixIn, TCPServer, BaseRequestHandler

from wsgit.wsgi import WSGIHandler, Environ

class Server(ThreadingMixIn, TCPServer):
    def __init__(self, addr, handler, app):
        self.app = app
        self.connected_handlers = []
        TCPServer.__init__(self, addr, handler)

    @classmethod
    def run_server(cls, addr, app):
        bson.patch_socket()
        server = cls(addr, WSGITRequestHandler, app)
        threading.Thread(target=server.serve_forever).start()
        return server

class WSGITRequestHandler(BaseRequestHandler):
    def setup(self):
        self.conn = self.request
        self.server.connected_handlers.append(self)

    def handle(self):
        while True:
            try:
                obj = self.conn.recvobj()
            except Exception:
                logger.debug('Bad Request. Not bson protocol.')
            if obj == None:
                break
            environ = Environ(obj)
            wsgi_handler = WSGIHandler()
            obj = wsgi_handler.call_application(self.server.app, 
                                                environ.get_dict())
            self.conn.send(obj)


    def finish(self):
        self.conn.close()
