# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 16:37:22 2016

@author: Tatiana Tassi
"""

import tornado.web


class PatientListHandler(tornado.web.RequestHandler):
    
    def get(self):
        patients_result = self.application.db.fetch_patients()
        patients_list = []
        if patients_result:
            for patient in patients_result:
                patients_list.append({
                    "id": patient[0],
                    "code": patient[1]
                })
        self.write({"patients": patients_list})
        
    def post(self):
        code = self.get_body_argument("code")
        self.application.db.add_patient(code)