import os
import sqlite3
import pandas as pd

# Main class for parsing ABC music files
class ABCParser:
    # Initialize with database name, default is tunes.db
    def __init__(self, db_name: str = "tunes.db"):
        self.db_name = db_name
        self.init_database()