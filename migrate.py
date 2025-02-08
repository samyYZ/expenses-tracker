import sqlite3

def migrate():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Example: Adding a new column if it doesn't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'new_column' not in columns:  # Example: Replace 'new_column' with any actual column name
        cursor.execute("ALTER TABLE users ADD COLUMN new_column TEXT")
        print("Added new column: new_column")

    conn.close()

migrate()
