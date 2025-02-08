import sqlite3

def check_column_exists():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Check if the expenses_json column exists
    cursor.execute("PRAGMA table_info(users)")  # Get table info for 'users'
    columns = cursor.fetchall()

    # Extract column names
    column_names = [column[1] for column in columns]

    # Check if 'expenses_json' column exists
    if 'expenses_json' in column_names:
        print("The 'expenses_json' column exists in the 'users' table.")
    else:
        print("The 'expenses_json' column does NOT exist in the 'users' table.")

    conn.close()

# Run the check
if __name__ == '__main__':
    check_column_exists()
