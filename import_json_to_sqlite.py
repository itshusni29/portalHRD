import sqlite3
import json

def import_json_to_sqlite(json_file, db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main_visitor (
        timestamp TEXT,
        ip_address TEXT,
        id INTEGER PRIMARY KEY
    )
    ''')
    
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Insert data into SQLite
    for row in data['rows']:
        cursor.execute('''
        INSERT OR IGNORE INTO main_visitor (timestamp, ip_address, id)
        VALUES (?, ?, ?)
        ''', (row[0], row[1], row[2]))
    
    # Commit and close connection
    conn.commit()
    conn.close()

# Example usage
import_json_to_sqlite('data.json', 'database.db')
