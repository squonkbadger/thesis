# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 21:57:47 2016

@author: Tatiana Tassi
"""

import tornado.web


class SessionHandler(tornado.web.RequestHandler):
    
    def get(self, session_id):
        session = self.application.db.fetch_session(session_id)
        if session:
            self.write(
                {
                    "id": session[0], 
                    "start_time": session[1], 
                    "end_time": session[2], 
                    "course_id":session[3], 
                    "instructor_id":session[4], 
                    "patient_id":session[5], 
                    "sample_rate":session[6], 
                    "resolution":session[7]
                }
            )

    def post(self, session_id):
        course_id = self.get_body_argument("course_id")
        instructor_id = self.get_body_argument("instructor_id")
        patient_id = self.get_body_argument("patient_id")
        sample_rate = self.get_body_argument("sample_rate")
        resolution = self.get_body_argument("resolution")
        self.application.db.edit_session(
            session_id, 
            course_id, 
            instructor_id, 
            patient_id, 
            sample_rate, 
            resolution
        )