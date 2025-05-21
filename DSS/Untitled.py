import requests
from bs4 import BeautifulSoup

def fetch_weather_data(city):
    # Replace with the actual URL of the weather website
    url = f"https://www.oneweather.com/{cITY}/daily/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract weather data (update selectors based on the website's structure)
        weather_data = []
        for day in soup.select('.day-forecast'):  # Update this selector
            date = day.select_one('.date').text.strip()
            temp = day.select_one('.temp').text.strip()
            condition = day.select_one('.condition').text.strip()
            weather_data.append((date, temp, condition))
        
        return weather_data
    else:
        print("Failed to fetch weather data")
        return None