import sqlite3

# Connect or create the DB
conn = sqlite3.connect('long_term_memory.db')
cursor = conn.cursor()

# Create a table for storing user interactions
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    interaction_type TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit and close
conn.commit()
conn.close()
