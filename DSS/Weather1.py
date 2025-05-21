import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import http.client
import json
import datetime
import os
import csv
from statistics import mean

# Fetch weather data function using http.client
def fetch_weather_data(city):
    api_key = "31a92b1435beb4d4ddee94bac265e232" 
    conn = http.client.HTTPSConnection("api.openweathermap.org")
    url = f"/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            messagebox.showerror("Error", f"Failed to fetch weather data. Status Code: {response.status}")
            return None

        data = json.loads(response.read().decode())

        if "list" not in data:
            messagebox.showerror("Error", f"API Error: {data.get('message', 'Unknown error')}")
            return None

        weather_data = {}

        # Select closest forecast to 12:00 PM (UTC) for each day
        for entry in data['list']:
            date = datetime.datetime.fromtimestamp(entry['dt'], datetime.timezone.utc).strftime('%Y-%m-%d')
            time = datetime.datetime.fromtimestamp(entry['dt'], datetime.timezone.utc).strftime('%H:%M:%S')
            temp = entry['main']['temp']
            humidity = entry['main']['humidity'] * 10 

            if date not in weather_data or abs(int(time[:2]) - 12) < abs(int(weather_data[date][0][:2]) - 12):
                weather_data[date] = (time, temp, humidity)

        return [(date, f"{temp}°C", f"{humidity}mm") for date, (_, temp, humidity) in sorted(weather_data.items())]

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

# weather data from data.csv and calculate monthly averages
def calculate_monthly_forecast():
    try:
        historical_data = []
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure the required columns exist
                if all(key in row for key in ['Year', 'Month', 'Temperature', 'Humidity']):
                    historical_data.append({
                        "Year": int(row['Year']),
                        "Month": int(row['Month']),
                        "Temperature": float(row['Temperature']),
                        "Humidity": float(row['Humidity'])
                    })
                else:
                    messagebox.showerror("Error", "Data file is missing required columns.")
                    return None, None, None

        # Group data by month and calculate averages
        monthly_data = {}
        for entry in historical_data:
            month = entry["Month"]
            if month not in monthly_data:
                monthly_data[month] = {"Temperature": [], "Humidity": []}
            monthly_data[month]["Temperature"].append(entry["Temperature"])
            monthly_data[month]["Humidity"].append(entry["Humidity"])

        # Calculate monthly averages
        monthly_forecast = []
        for month, values in monthly_data.items():
            avg_temp = mean(values["Temperature"])
            avg_humidity = mean(values["Humidity"])
            monthly_forecast.append((month, avg_temp, avg_humidity))

        # Sort by month
        monthly_forecast.sort(key=lambda x: x[0])

        # Summarize the general temperature and humidity for the year
        avg_temp_year = mean([x[1] for x in monthly_forecast])
        avg_humidity_year = mean([x[2] for x in monthly_forecast])

        return monthly_forecast, avg_temp_year, avg_humidity_year

    except Exception as e:
        messagebox.showerror("Error", f"Could not process data file: {e}")
        return None, None, None

# Display weather in Treeview
def display_weather():
    city = entry_city.get().strip()
    if city:
        weather_data = fetch_weather_data(city)
        if weather_data:
            tree.delete(*tree.get_children())  # Clear old data
            for data in weather_data:
                tree.insert("", "end", values=data)
        else:
            messagebox.showwarning("Error", "Could not retrieve weather data.")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

    # Display monthly forecast based on historical data
    monthly_forecast, avg_temp, avg_humidity = calculate_monthly_forecast()
    if monthly_forecast is not None:
        tree_monthly.delete(*tree_monthly.get_children())  # Clear old data
        for month, temp, humidity in monthly_forecast:
            tree_monthly.insert("", "end", values=(month, f"{temp:.2f}°C", f"{humidity:.2f}mm"))

        # Display summary
        lbl_summary.config(text=f"Yearly Avg Temperature: {avg_temp:.2f}°C, Yearly Avg Humidity: {avg_humidity:.2f}mm")

# Function to open Advice1.py
def open_advice_script():
    try:
        os.system("python Advice1.py")  # Run Advice1.py
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Advice1.py: {e}")

# GUI setup
root = tk.Tk()
root.title("Weather Data Interface")
root.geometry("700x800")  # Adjusted window size
root.configure(bg="blue")  # Set outer frame background color to blue

# Outer frame
outer_frame = tk.Frame(root, bg="lightgreen", relief=tk.RAISED, borderwidth=2)
outer_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# City input field (innermost frame)
frame = tk.Frame(outer_frame, bg="lightgreen")
frame.pack(pady=10, anchor="center")  # Center the frame

tk.Label(frame, text="Enter City:", font=("Arial", 12), bg="lightgreen").pack(side=tk.LEFT, padx=5)
entry_city = tk.Entry(frame, width=20, font=("Arial", 12))
entry_city.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Get Weather", font=("Arial", 12), bg="darkgreen", fg="white", command=display_weather).pack(side=tk.LEFT, padx=5)

# Button to open Advice1.py
tk.Button(outer_frame, text="Advice", font=("Arial", 10), bg="blue", fg="white", command=open_advice_script).pack(pady=10)

# Table to display weather data
columns = ("Date", "Temperature", "Humidity")
tree = ttk.Treeview(outer_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Table to display monthly forecast
tk.Label(outer_frame, text="Monthly Forecast (Based on Historical Data)", font=("Arial", 12), bg="lightgreen").pack(pady=10)
columns_monthly = ("Month", "Avg Temperature", "Avg Humidity")
tree_monthly = ttk.Treeview(outer_frame, columns=columns_monthly, show="headings", height=12)
for col in columns_monthly:
    tree_monthly.heading(col, text=col)
    tree_monthly.column(col, anchor="center", width=150)

tree_monthly.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label to display yearly summary
lbl_summary = tk.Label(outer_frame, text="", font=("Arial", 12), bg="lightgreen")
lbl_summary.pack(pady=10)

root.mainloop()