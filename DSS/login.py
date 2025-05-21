import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

# Function to verify login credentials
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            open_weather_file()  # Redirect to Weather1.py
        else:
            messagebox.showwarning("Error", "Invalid username or password")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to open the Weather1.py file
def open_weather_file():
    try:
        # Open the Weather1.py file using Python
        subprocess.run(["python", "Weather1.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Weather1.py: {e}")

# GUI setup for login
root = tk.Tk()
root.title("Login Interface")
root.configure(bg="blue")  # Set background color to blue for the outer frame

# Outer frame
outer_frame = tk.Frame(root, bg="blue", padx=60, pady=60)
outer_frame.pack(expand=True, fill="both")

# Inner frame
inner_frame = tk.Frame(outer_frame, bg="green", padx=30, pady=30)
inner_frame.pack(expand=True)

# Username label and entry
tk.Label(inner_frame, text="Username", bg="green", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(inner_frame, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10, pady=10)

# Password label and entry
tk.Label(inner_frame, text="Password", bg="green", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(inner_frame, show="*", font=("Arial", 12))
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Login button
login_button = tk.Button(inner_frame, text="Login", command=login_user, bg="white", fg="green", font=("Arial", 12), width=10)
login_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()