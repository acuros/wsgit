from SocketServer import BaseRequestHandler
import bson

class ClientRequestHandler(BaseRequestHandler):
    def setup(self):
        self.server.connected_handlers.append(self)

    def handle(self):
        obj = self.request.recvobj()
        print obj
