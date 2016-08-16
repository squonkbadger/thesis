# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 23:37:11 2016

@author: Badger
"""

import tornado.web


class SessionListHandler(tornado.web.RequestHandler):

    def get(self):
        sessions_result = self.application.db.fetch_sessions()
        sessions_list = []
        if sessions_result:
            for session in  sessions_result:
                sessions_list.append({
                    "id": session[0],
                    "start_time": session[1],
                    "end_time": session[2],
                    "course_id":session[3],
                    "instructor_id":session[4],
                    "patient_id":session[5],
                    "sample_rate":session[6],
                    "resolution":session[7]
                })
        self.write({"sessions": sessions_list})