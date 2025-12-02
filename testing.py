import os
import sqlite3
import pandas as pd

class ABCParser:
    def __init__(self, db_name: str = "tunes.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
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
    
    def parse_abc_file(self, file_path: str):
        tunes = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            # Split by X: to separate individual tunes
            tune_blocks = content.split('X:')
            
            for block in tune_blocks:
                if block.strip():
                    lines = block.strip().split('\n')
                    tune_data = {
                        'title': 'Unknown',
                        'tune_type': 'Unknown',
                        'key': '',
                        'meter': '',
                        'abc_notation': block[:200] + "..." if len(block) > 200 else block
                    }
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('T:'):
                            tune_data['title'] = line[2:].strip()
                        elif line.startswith('R:'):
                            tune_data['tune_type'] = line[2:].strip()
                        elif line.startswith('K:'):
                            tune_data['key'] = line[2:].strip()
                        elif line.startswith('M:'):
                            tune_data['meter'] = line[2:].strip()
                    
                    if tune_data['title'] != 'Unknown':
                        tunes.append(tune_data)
                        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return tunes
    
    def process_abc_directory(self, base_dir: str = r"C:\Users\Mohammedrog\Downloads\dcp25-assignment\abc_books"):
        all_tunes = []
        
        if not os.path.exists(base_dir):
            print(f"ERROR: Folder not found at {base_dir}")
            return all_tunes
        
        print(f"Processing files from: {base_dir}")
        
        # Look for numbered folders (0, 1, 2, etc.) inside abc_books
        for folder_name in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder_name)
            
            if os.path.isdir(folder_path):
                try:
                    book_num = int(folder_name)  # Folder name is the book number
                except:
                    continue  # Skip non-numbered folders
                
                print(f"Processing book {book_num}...")
                
                # Process all .abc files in this book folder
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.abc'):
                        file_path = os.path.join(folder_path, file_name)
                        
                        tunes = self.parse_abc_file(file_path)
                        for tune in tunes:
                            tune['book_number'] = book_num
                            tune['file_name'] = file_name
                            all_tunes.append(tune)
                        
                        print(f"  - {file_name} -> {len(tunes)} tunes")
        
        return all_tunes
    
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
    
    def load_tunes_from_database(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql("SELECT * FROM tunes", conn)
        conn.close()
        return df

def get_tunes_by_book(df, book_number):
    return df[df['book_number'] == book_number]

def get_tunes_by_type(df, tune_type):
    return df[df['tune_type'].str.contains(tune_type, case=False, na=False)]

def search_tunes(df, search_term):
    return df[df['title'].str.contains(search_term, case=False, na=False)]

def main():
    parser = ABCParser()
    
    print("=== ABC File Parser ===")
    tunes = parser.process_abc_directory()
    
    if not tunes:
        print("No tunes found!")
        return
    
    parser.save_to_database(tunes)
    df = parser.load_tunes_from_database()
    print(f"✅ Success! Loaded {len(df)} tunes")
    
    while True:
        print("\n1. Search by title")
        print("2. Get by book number") 
        print("3. Get by tune type")
        print("4. Show all")
        print("5. Exit")
        
        choice = input("Choose 1-5: ")
        
        if choice == '1':
            term = input("Search title: ")
            results = search_tunes(df, term)
            print(f"Found {len(results)} tunes:")
            for _, tune in results.iterrows():
                print(f"  - {tune['title']} (Book {tune['book_number']})")
            
        elif choice == '2':
            book = input("Book number: ")
            results = get_tunes_by_book(df, int(book))
            print(f"Book {book} has {len(results)} tunes:")
            for _, tune in results.iterrows():
                print(f"  - {tune['title']} ({tune['tune_type']})")
            
        elif choice == '3':
            t_type = input("Tune type: ")
            results = get_tunes_by_type(df, t_type)
            print(f"Found {len(results)} {t_type} tunes:")
            for _, tune in results.iterrows():
                print(f"  - {tune['title']} (Book {tune['book_number']})")
            
        elif choice == '4':
            print(f"All {len(df)} tunes:")
            for _, tune in df.iterrows():
                print(f"  - {tune['title']} | Book {tune['book_number']} | {tune['tune_type']}")
            
        elif choice == '5':
            break

if __name__ == "__main__":
    main()