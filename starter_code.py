import os
import sqlite3
import pandas as pd

# Main class for parsing ABC music files
class ABCParser:
    # Initialize with database name, default is tunes.db
    def __init__(self, db_name: str = "tunes.db"):
        self.db_name = db_name
        self.init_database()
    
    # Creates the database table if it doesn't exist
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
    
    # Parses a single ABC file and extracts all tunes from it
    def parse_abc_file(self, file_path: str):
        tunes = []
        try:
            # Read the ABC file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            # ABC files use 'X:' to separate multiple tunes
            tune_blocks = content.split('X:')
            
            for block in tune_blocks:
                if block.strip():
                    lines = block.strip().split('\n')
                    # Default tune data structure
                    tune_data = {
                        'title': 'Unknown',
                        'tune_type': 'Unknown',
                        'key': '',
                        'meter': '',
                        'abc_notation': block[:200] + "..." if len(block) > 200 else block
                    }
                    
                    # Parse ABC metadata lines
                    for line in lines:
                        line = line.strip()
                        if line.startswith('T:'):  # Title
                            tune_data['title'] = line[2:].strip()
                        elif line.startswith('R:'):  # Tune type (jig, reel, etc.)
                            tune_data['tune_type'] = line[2:].strip()
                        elif line.startswith('K:'):  # Musical key (D, G, etc.)
                            tune_data['key'] = line[2:].strip()
                        elif line.startswith('M:'):  # Meter/time signature
                            tune_data['meter'] = line[2:].strip()
                    
                    # Only add tunes with a valid title
                    if tune_data['title'] != 'Unknown':
                        tunes.append(tune_data)
                        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return tunes
    
    # Processes all ABC files in the directory structure
    def process_abc_directory(self, base_dir: str = r"C:\Users\Mohammedrog\Downloads\dcp25-assignment\abc_books"):
        all_tunes = []
        
        if not os.path.exists(base_dir):
            print(f"ERROR: Folder not found at {base_dir}")
            return all_tunes
        
        print(f"Processing files from: {base_dir}")
        
        # Each numbered folder is a book (0, 1, 2, etc.)
        for folder_name in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder_name)
            
            if os.path.isdir(folder_path):
                try:
                    book_num = int(folder_name)  # Convert folder name to book number
                except:
                    continue  # Skip non-numeric folders
                
                print(f"Processing book {book_num}...")
                
                # Process all .abc files in this book folder
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.abc'):
                        file_path = os.path.join(folder_path, file_name)
                        tunes = self.parse_abc_file(file_path)
                        
                        # Add book info to each tune
                        for tune in tunes:
                            tune['book_number'] = book_num
                            tune['file_name'] = file_name
                            all_tunes.append(tune)
                        
                        print(f"  - {file_name} -> {len(tunes)} tunes")
        
        return all_tunes
    
    # Saves all parsed tunes to the database
    def save_to_database(self, tunes: list):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for tune in tunes:
            cursor.execute('''
                INSERT INTO tunes (book_number, file_name, title, tune_type, key, meter, abc_notation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tune['book_number'], tune['file_name'], tune['title'],
                tune['tune_type'], tune['key'], tune['meter'], tune['abc_notation']
            ))
        
        conn.commit()
        conn.close()
        print(f"Saved {len(tunes)} tunes to database")
        
    # Loads tunes from database into pandas DataFrame
    def load_tunes_from_database(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql("SELECT * FROM tunes", conn)
        conn.close()
        return df
    
    # Returns tunes from a specific book
def get_tunes_by_book(df, book_number):
    return df[df['book_number'] == book_number]

# Returns tunes of a specific type (e.g., jig, reel)
def get_tunes_by_type(df, tune_type):
    return df[df['tune_type'].str.contains(tune_type, case=False, na=False)]

