import os
import psycopg2
from psycopg2.extras import RealDictCursor
import config

class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(config.DATABASE_URL)
            self.create_tables()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
            
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create students table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            student_id VARCHAR(20) UNIQUE NOT NULL,
            impairment_type INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create progress table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id SERIAL PRIMARY KEY,
            student_id VARCHAR(20) REFERENCES students(student_id),
            topic VARCHAR(50) NOT NULL,
            level FLOAT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create performance_history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_history (
            id SERIAL PRIMARY KEY,
            student_id VARCHAR(20) REFERENCES students(student_id),
            topic VARCHAR(50) NOT NULL,
            question_type VARCHAR(50) NOT NULL,
            difficulty INTEGER NOT NULL,
            is_correct BOOLEAN NOT NULL,
            response_time FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
        cursor.close()