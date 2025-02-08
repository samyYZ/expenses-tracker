import sqlite3

def check_schema():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Check for table existence
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    required_columns = ['id', 'name', 'income', 'expense_limit', 'expenses_json']

    missing_columns = [col for col in required_columns if col not in columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
    else:
        print("All required columns exist.")

    conn.close()

check_schema()
