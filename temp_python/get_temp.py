# get_temp
import requests
import time
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

api_key = "e159d8b19903e1acaad8c920d3a8ea9e"
city_name = "Ludhiana"
duration_limit_hours = 0.1
start_time = time.time()  # Record the start time
temperature_data = []

while time.time() - start_time < duration_limit_hours * 3600:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature_celsius = weather_data['main']['temp'] - 273.15
        timestamp = datetime.now()

        # Append data to the list
        temperature_data.append({
            'timestamp': timestamp,
            'temperature': temperature_celsius
        })

        print(f"At {timestamp}: Temperature is {temperature_celsius:.2f} °C")

        with open("temperature_data.txt", "w") as file:
            # Use the custom DateTimeEncoder
            json.dump(temperature_data, file, cls=DateTimeEncoder)

        

        # Delay for half an hour
        time.sleep(50)  # 1800 seconds = 30 minutes

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        break
print("File temperature_data.txt has been written.")