import bson
import threading
from SocketServer import ForkingMixIn, TCPServer

from django.conf import settings

from imdjango.network.handler import IMRequestHandler

class IMServer(ForkingMixIn, TCPServer):
    _instance = None
    connected_handlers=[]

    @classmethod
    def start_server(cls, host=getattr(settings, 'MOBILE_HOST', '0.0.0.0'), port=getattr(settings, 'MOBILE_PORT', 9338)):
        bson.patch_socket()
        server = cls((host, int(port)), IMRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
            
if __name__ == '__main__':
    IMServer.start_server()
