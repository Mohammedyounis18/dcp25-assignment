import os
import sqlite3
import pandas as pd

# Main class for parsing ABC music files
class ABCParser:
    # Initialize with database name, default is tunes.db
    def __init__(self, db_name: str = "tunes.db"):
        self.db_name = db_name
        self.init_database()
        
         # Creates the database table 
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Table stores: ID, book number, filename, title, type, key, meter, and ABC notation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_number INTEGER,
                file_name TEXT,
                title TEXT,
                tune_type TEXT,
                key TEXT,
                meter TEXT,
                abc_notation TEXT
            )
        ''')
        conn.commit()
        conn.close()