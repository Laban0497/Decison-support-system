import tkinter as tk
from tkinter import simpledialog
import math

def recommend_crop(temperature, humidity):
    # Crops with their temperature and humidity ranges
    crop_data = [
        {"name": "Tea (9 months)", "temp_range": (18, 24), "humidity":  2500},
        {"name": "Coffee (12 months)", "temp_range": (18, 24), "humidity":  2000},
        {"name": "Avocado (24 months)", "temp_range": (20, 30), "humidity":  1200},
        {"name": "Mangoes (36 months)", "temp_range": (20, 30), "humidity":  1000},
        {"name": "Maize (3 months)", "temp_range": (20, 25), "humidity":  1200},
        {"name": "Arrow root (6 months)", "temp_range": (20, 30), "humidity":  1500},
        {"name": "Sweet potatoes (4 months)", "temp_range": (24, 37), "humidity":  1000},
        {"name": "Irish potatoes (3 months)", "temp_range": (15, 20), "humidity":  1200},
        {"name": "Cassava (12 months)", "temp_range": (25, 30), "humidity":  1500},
    ]

    # Find exact matches
    crops = [
        crop["name"]
        for crop in crop_data
        if crop["temp_range"][0] < temperature < crop["temp_range"][1] and humidity < crop["humidity"]
    ]

    if crops:
        return crops, None

    # Find the closest crop if no exact match
    closest_crop = None
    closest_distance = float("inf")
    for crop in crop_data:
        temp_mid = (crop["temp_range"][0] + crop["temp_range"][1]) / 2
        distance = math.sqrt((temperature - temp_mid) ** 2 + (humidity - crop["humidity"]) ** 2)
        if distance < closest_distance:
            closest_distance = distance
            closest_crop = crop

    if closest_crop:
        return None, closest_crop
    return None, None

def on_submit():
    temp = float(entry_temp.get())
    humid = float(entry_humid.get())
    crops, closest_crop = recommend_crop(temp, humid)

    if crops:
        result_label.config(text="Recommended Crops: " + ", ".join(crops))
    elif closest_crop:
        result_label.config(
            text=f"No suitable crop found. Closest match: {closest_crop['name']}.\n"
                 f"Recommended temperature: {closest_crop['temp_range'][0]}°C to {closest_crop['temp_range'][1]}°C, "
                 f"Humidity: < {closest_crop['humidity']}.\n"
                 "Please wait for suitable weather conditions."
        )
    else:
        result_label.config(text="No suitable crop found.")

def exit_to_login():
    root.destroy()
    import login  # Assuming login.py is in the same directory

# Creating main window
root = tk.Tk()
root.title("Crop Recommendation System")
root.geometry("600x600")  # Increased window size
root.configure(bg="blue")  # Set the background color

# Outer frame for centering content
outer_frame = tk.Frame(root, bg="lightgreen", width=500, height=500)
outer_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Styling options
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Adding widgets inside the outer frame
tk.Label(outer_frame, text="Enter Temperature (°C):", font=label_font, bg="white").pack(pady=10)
entry_temp = tk.Entry(outer_frame, font=entry_font)
entry_temp.pack(pady=5)

tk.Label(outer_frame, text="Enter Humidity (mm):", font=label_font, bg="white").pack(pady=10)
entry_humid = tk.Entry(outer_frame, font=entry_font)
entry_humid.pack(pady=5)

submit_button = tk.Button(outer_frame, text="Submit", font=button_font, bg="green", fg="white", command=on_submit)
submit_button.pack(pady=15)

exit_button = tk.Button(outer_frame, text="Exit", font=button_font, bg="red", fg="white", command=exit_to_login)
exit_button.pack(pady=10)

result_label = tk.Label(outer_frame, text="", font=label_font, bg="lightgreen", wraplength=400, justify="left")
result_label.pack(pady=10)

root.mainloop()