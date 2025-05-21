import http.client
import json
import datetime

# Function to fetch weather data for a given city
def fetch_weather_data(city, country_code=None):
    api_key = "31a92b1435beb4d4ddee94bac265e232"  # Replace with your OpenWeatherMap API key
    location = f"{city},{country_code}" if country_code else city
    conn = http.client.HTTPSConnection("api.openweathermap.org")
    url = f"/data/2.5/forecast?q={location}&appid={api_key}&units=metric"

    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print(f"Error: {response.status} {response.reason}")
            return None

        data = json.loads(response.read().decode())

        if "list" not in data:
            print(f"Error for {city}: {data.get('message', 'Unknown error')}")
            return None

        weather_data = {}

        # Iterate through forecast data and select the closest entry to 12:00 PM (UTC)
        for entry in data['list']:
            date = datetime.datetime.fromtimestamp(entry['dt'], datetime.timezone.utc).strftime('%Y-%m-%d')
            time = datetime.datetime.fromtimestamp(entry['dt'], datetime.timezone.utc).strftime('%H:%M:%S')
            temp = entry['main']['temp']
            condition = entry['weather'][0]['description']

            # Store the best forecast for 12:00 PM UTC
            if date not in weather_data or abs(int(time[:2]) - 12) < abs(int(weather_data[date][0][:2]) - 12):
                weather_data[date] = (time, temp, condition)

        # Convert dictionary to sorted list of tuples
        daily_forecast = [(date, f"{temp}°C", condition) for date, (_, temp, condition) in sorted(weather_data.items())]
        return daily_forecast

    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to fetch weather for multiple cities
def fetch_weather_for_multiple_cities(cities):
    all_forecasts = {}
    for city, country in cities:
        forecast = fetch_weather_data(city, country)
        if forecast:
            all_forecasts[f"{city}, {country}"] = forecast
    return all_forecasts

# Example cities with country codes (Including Murang'a, Kenya)
cities = [
    ("London", "GB"),
    ("New York", "US"),
    ("Tokyo", "JP"),
    ("Nairobi", "KE"),
    ("Sydney", "AU"),
    ("Berlin", "DE"),
    ("Murang'a", "KE")  # 🔹 Added Murang'a County, Kenya
]

# Fetch weather for multiple cities
weather_reports = fetch_weather_for_multiple_cities(cities)

# Display results
for city, forecast in weather_reports.items():
    print(f"\n5-Day Weather Forecast for {city}:")
    for day in forecast:
        print(f"Date: {day[0]}, Temperature: {day[1]}, Condition: {day[2]}")