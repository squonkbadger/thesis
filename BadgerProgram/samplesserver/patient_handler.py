# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 19:09:45 2016

@author: Badger
"""

import tornado.web


class PatientHandler(tornado.web.RequestHandler):
    
    def get(self, patient_id):
        patient = self.application.db.fetch_patient(patient_id)
        if patient:
            self.write({"id": patient[0], "code": patient[1]})
            
    def post(self, patient_id):
        code = self.get_body_argument("code")
        self.application.db.edit_patient(code, patient_id)