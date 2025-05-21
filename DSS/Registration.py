import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import subprocess  # Import subprocess to execute external Python scripts

# Database setup
def create_db():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

# Function to validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to register a new user
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    if not username or not password or not email:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    if not is_valid_email(email):
        messagebox.showwarning("Input Error", "Please enter a valid email address")
        return

    try:
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, password, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email or Username already registered")

# Function to navigate to login page
def go_to_login():
    root.destroy()  # Close the current registration window
    try:
        # Open the Login.py file using Python
        subprocess.run(["python", "login.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Login.py: {e}")

# GUI setup
root = tk.Tk()
root.title("Registration Interface")
root.configure(bg="blue")  # Outer frame background color

# Outer frame
outer_frame = tk.Frame(root, bg="blue", padx=60, pady=60)
outer_frame.pack(expand=True, fill="both")

# Inner frame
inner_frame = tk.Frame(outer_frame, bg="green", padx=30, pady=30)
inner_frame.pack(expand=True)

# Widgets inside the inner frame
tk.Label(inner_frame, text="Username", bg="green", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(inner_frame, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(inner_frame, text="Password", bg="green", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(inner_frame, show="*", font=("Arial", 12))
entry_password.grid(row=1, column=1, padx=10, pady=10)

tk.Label(inner_frame, text="Email", bg="green", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(inner_frame, font=("Arial", 12))
entry_email.grid(row=2, column=1, padx=10, pady=10)

# Register button
tk.Button(inner_frame, text="Register", command=register_user, bg="white", fg="green", font=("Arial", 12), width=20).grid(row=3, column=0, columnspan=2, pady=10)

# Go to Login button
tk.Button(inner_frame, text="Go to Login", command=go_to_login, bg="white", fg="green", font=("Arial", 12), width=20).grid(row=4, column=0, columnspan=2, pady=10)

create_db()  # Ensure the database and table exist
root.mainloop()