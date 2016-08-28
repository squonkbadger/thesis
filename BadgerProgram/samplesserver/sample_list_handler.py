# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:44:21 2016

@author: Tatiana Tassi
"""

import tornado.web


class SampleListHandler(tornado.web.RequestHandler):

    def get(self, session_id):
        samples_result = self.application.db.fetch_samples(session_id)
        samples_list = []
        if samples_result:
            for sample in  samples_result:
                samples_list.append({
                    "id": sample[0],
                    "order_number": sample[9],
                    "session_id": sample[10],
                    "channel_data": sample[1:9]
                })
        self.write({"samples": samples_list})