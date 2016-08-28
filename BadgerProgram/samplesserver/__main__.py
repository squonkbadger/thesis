# -*- coding: utf-8 -*-
"""
Created on Sun Aug 07 01:16:27 2016

@author: Tatiana Tassi
"""

import logging
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import os

import samplesserver

define('host', type=str, default='127.0.0.1')
define('port', type=int, default=1912)

app_log = logging.getLogger('tornado.application')


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
    

parse_command_line()    

app_log.info('Running server on %s:%d', options.host, options.port)

app = make_app()
app.listen(options.port, options.host)
tornado.ioloop.IOLoop.current().start()