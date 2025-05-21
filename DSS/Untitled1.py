import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')
conn.commit()

# Function to register a new user
def register_user(username, password, email):
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username or email already exists.")

# Example usage
register_user("john_doe", "password123", "john@example.com")

# Close the connection when done
conn.close()