# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:22:16 2016

@author: Badger
"""

import tornado.web


class InstructorHandler(tornado.web.RequestHandler):
    
    def get(self, instructor_id):
        instructor = self.application.db.fetch_instructor(instructor_id)
        if instructor:
            self.write({
                "id": instructor[0], 
                "name": instructor[1], 
                "email": instructor[2]
            })
            
    def post(self, instructor_id):
        name = self.get_body_argument("name")
        email = self.get_body_argument("email")
        self.application.db.edit_instructor(instructor_id, name, email)