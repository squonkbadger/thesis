# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:37:29 2016

@author: Badger
"""

import tornado.web


class CourseHandler(tornado.web.RequestHandler):
    
    def get(self, course_id):
        course = self.application.db.fetch_course(course_id)
        if course:
            self.write({
                "id": course[0], 
                "name": course[2], 
                "code": course[3], 
                "credit_value": course[4]
            })
            
    def post(self, course_id):
        instructor_name = self.get_body_argument("instructor_name")
        name = self.get_body_argument("name")
        code = self.get_body_argument("code")
        credit_value = self.get_body_argument("credit_value")
        self.application.db.edit_patient(course_id, instructor_name, name, code, credit_value)