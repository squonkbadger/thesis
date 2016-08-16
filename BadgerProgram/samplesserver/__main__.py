# -*- coding: utf-8 -*-
"""
Created on Sun Aug 07 01:16:27 2016

@author: Badger
"""

import tornado.ioloop
import tornado.web
import os

import samplesserver


def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": True
    }
    
    app = tornado.web.Application([
        (r"/api/samples", samplesserver.SampleReceiver),
        (r"/api/sessions", samplesserver.SessionListHandler),
        (r"/api/sessions/(\d+)/samples", samplesserver.SampleListHandler),
        (r"/api/courses", samplesserver.CourseListHandler),
        (r"/api/instructors", samplesserver.InstructorListHandler),
        (r"/api/patients", samplesserver.PatientListHandler),
        (r"/api/patients/(\d+)", samplesserver.PatientHandler),
        (r"/api/instructors/(\d+)", samplesserver.InstructorHandler),
        (r"/api/courses/(\d+)", samplesserver.CourseHandler),
        (r"/api/sessions/(\d+)", samplesserver.SessionHandler),
        (
            r"/(.*)", tornado.web.StaticFileHandler,
            {
                "path": settings['static_path'],
                "default_filename": "index.html"
            }
        ),
    ], **settings)
    app.db = samplesserver.Database()
    return app
    
    
app = make_app()
app.listen(1912, "127.0.0.1")
tornado.ioloop.IOLoop.current().start()
    
    
"""

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://127.0.0.1:1912")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(1912, factory)
    reactor.run()

"""

"""
import socket


tcp_ip = "127.0.0.1"
tcp_port = 1912
buffer_size = 250


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((tcp_ip, tcp_port))
sock.listen(1)

conn, addr = sock.accept()
print "Connection address:", addr
while 1:
    data = conn.recv(buffer_size)
    if not data: break
    print "received data:", data
    conn.send(data)
conn.close()
"""