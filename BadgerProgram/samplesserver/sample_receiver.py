# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 23:30:24 2016

@author: Badger
"""

import tornado.websocket
import tornado.escape


class SampleReceiver(tornado.websocket.WebSocketHandler):
    
    def open(self):
        session_id = self.application.db.create_session()
        self.session_id = session_id
        
    def on_message(self, json_sample):
        dict_sample = tornado.escape.json_decode(json_sample)
        self.application.db.create_sample(self.session_id, dict_sample)
        
    def on_close(self):
        self.application.db.finalise_session(self.session_id)