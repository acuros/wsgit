import unittest
import bson
from threading import Thread
from wsgit.server import Server
from tests.applications import application1 as app
from socket import socket, SOCK_STREAM, AF_INET

class TestServer(unittest.TestCase):
    def test_server(self):
        bson.patch_socket()
        server = Server.run_server(('127.0.0.1', 9338), app)
        conn = socket(AF_INET, SOCK_STREAM)
        conn.connect(('127.0.0.1', 9338))
        conn.sendobj({'url':'/'})
        self.assertEqual(conn.recvobj(), dict(status=dict(reason='OK', code='200')))
        server.shutdown()
