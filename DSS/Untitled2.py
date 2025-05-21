import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Function to check login credentials
def login_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

# Example usage
login_user("john_doe", "password123")

# Close the connection when done
conn.close()