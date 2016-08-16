# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 23:42:12 2016

@author: Badger
"""

import sqlite3
import datetime

class Database(object):
    
    def __init__(self):
        self.conn = sqlite3.connect("samples_server.db",
                                    detect_types=sqlite3.PARSE_DECLTYPES)
        self._create_tables()
        
    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                course_id INTEGER,
                instructor_id INTEGER,
                patient_id INTEGER,
                sample_rate REAL,
                resolution REAL,
                FOREIGN KEY(course_id) REFERENCES courses(id),
                FOREIGN KEY(instructor_id) REFERENCES instructors(id),
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                channel1 REAL NOT NULL,
                channel2 REAL NOT NULL, 
                channel3 REAL NOT NULL,
                channel4 REAL NOT NULL, 
                channel5 REAL NOT NULL, 
                channel6 REAL NOT NULL, 
                channel7 REAL NOT NULL,
                channel8 REAL NOT NULL, 
                order_number INTEGER NOT NULL,
                session_id INTEGER NOT NULL, 
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            )        
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL,
                email TEXT
            )        
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                instructor_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                credit_value INT,
                FOREIGN KEY(instructor_id) REFERENCES instructor(id)
            )        
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                code TEXT
            )        
        """)
        self.conn.commit()
        

    def create_session(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sessions(start_time, sample_rate) VALUES (?,?)
        """, (datetime.datetime.now(),250))
        self.conn.commit()        
        session_id = cursor.lastrowid
        return session_id
    
    def create_sample(self, session_id, sample):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO samples(
                channel1,
                channel2,
                channel3,
                channel4,
                channel5,
                channel6,
                channel7,
                channel8,
                order_number,
                session_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?)        
        """, (
            sample["channel_data"][0],
            sample["channel_data"][1],
            sample["channel_data"][2],
            sample["channel_data"][3],
            sample["channel_data"][4],
            sample["channel_data"][5],
            sample["channel_data"][6],
            sample["channel_data"][7],
            sample["order_number"],
            session_id
            )
        )
        self.conn.commit()
        sample_id = cursor.lastrowid
        return sample_id
        
    def finalise_session(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions
            SET end_time = ?
            WHERE id = ?
        """, (datetime.datetime.now(), session_id))
        self.conn.commit()
        
    def fetch_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM sessions
        """)
        sessions = cursor.fetchall()
        return sessions
    
    def fetch_session(self, session_id): 
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM sessions
            WHERE id = ?
        """, session_id)
        session = cursor.fetchone()
        return session
    
    def edit_session(self, session_id, course_id, instructor_id, patient_id, sample_rate, resolution):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions
            SET 
                course_id = ?, 
                instructor_id = ?,
                patient_id = ?,
                sample_rate = ?,
                resolution = ?
            
            WHERE id = ?
        """, (course_id, instructor_id, patient_id, sample_rate, resolution,session_id))
        
    def fetch_samples(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM samples
            WHERE session_id = ?
        """, session_id)
        samples = cursor.fetchall()
        return samples
        
    def fetch_courses(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM courses
        """)
        courses = cursor.fetchall()
        return courses
    
    def fetch_course(self, course_id): 
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM courses
            WHERE id = ?
        """, course_id)
        course = cursor.fetchone()
        return course
        
    def add_course(self, instructor_id, name, code, credit_value):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO courses (instructor_id, name, code, credit_value)
            VALUES (?,?,?,?)
        """, (instructor_id, name, code, credit_value))
        self.conn.commit()
    
    def edit_course(self, course_id, instructor_id, name, code, credit_value):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE courses
            SET instructor_id = ?, name = ?, code = ?, credit_value = ?
            WHERE id = ?
        """, (instructor_id, name, code, credit_value, course_id)) 
        self.conn.commit()
        
    def fetch_instructors(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM instructors
        """)
        instructors = cursor.fetchall()
        return instructors
    
    def add_instructor(self, name, email):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO instructors (name, email)
            VALUES (?,?)
        """, (name, email))
        self.conn.commit()
    
    def fetch_instructor(self, instructor_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM instructors
            WHERE id = ?
        """, instructor_id)
        instructor = cursor.fetchone()
        return instructor
    
    def edit_instructor(self, instructor_id, name, email):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE instructors
            SET name = ?, email = ?
            WHERE id = ?
        """, (name, email, instructor_id)) 
        self.conn.commit()
        
    def add_patient(self, code):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO patients (code)        
            VALUES (?)
        """, (code,))
        self.conn.commit()
    
    def edit_patient(self, code, patient_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE patients
            SET code = ?
            WHERE id = ?
        """, (code, patient_id)) 
        self.conn.commit()
        
    def fetch_patients(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM patients
        """)
        patients = cursor.fetchall()
        return patients
        
    def fetch_patient(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT *
            FROM patients
            WHERE id = ?
        """, patient_id)
        patient = cursor.fetchone()
        return patient