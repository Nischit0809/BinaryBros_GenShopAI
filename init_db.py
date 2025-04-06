import sqlite3

# Connect to SQLite (this creates the DB file if it doesn't exist)
conn = sqlite3.connect('memory.db')
cursor = conn.cursor()

# Create a table to store long-term memory (e.g., user interactions)
cursor.execute('''
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event TEXT NOT NULL,
    data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("✅ SQLite database and table initialized.")
