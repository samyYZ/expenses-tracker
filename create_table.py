import sqlite3

conn = sqlite3.connect('data.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    income REAL NOT NULL,
    expense_limit REAL NOT NULL,
    expenses_json TEXT
)
''')

conn.close()
print("Table created successfully.")

