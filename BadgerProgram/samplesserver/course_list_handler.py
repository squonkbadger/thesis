# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 16:14:11 2016

@author: Tatiana Tassi
"""

import tornado.web


class CourseListHandler(tornado.web.RequestHandler):
    
    def get(self):
        courses_result = self.application.db.fetch_courses()
        courses_list = []
        if courses_result:
            for course in courses_result:
                courses_list.append({
                    "id": course[0],
                    "instructor_id": course[1],
                    "name": course[2],
                    "code": course[3],
                    "credit_value": course[4]
                })
        self.write({"courses": courses_list})
        
    def post(self):
        instructor_id = self.get_body_argument("instructor_id")
        name = self.get_body_argument("name")
        code = self.get_body_argument("code")
        credit_value = self.get_body_argument("credits")
        self.application.db.add_course(instructor_id, name, code, credit_value)