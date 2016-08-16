# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 16:26:31 2016

@author: Badger
"""

import tornado.web


class InstructorListHandler(tornado.web.RequestHandler):
    
    def get(self):
        instructors_result = self.application.db.fetch_instructors()
        instructors_list = []
        if instructors_result:
            for instructor in instructors_result:
                instructors_list.append({
                    "id": instructor[0],
                    "name": instructor[1],
                    "email": instructor[2]
                })
        self.write({"instructors": instructors_list})
    
    def post(self):
        name = self.get_body_argument("name")
        email = self.get_body_argument("email")
        self.application.db.add_instructor(name, email)
        