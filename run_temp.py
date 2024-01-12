import time
import json
from datetime import datetime
import requests
from pyfiglet import Figlet

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def main():
    ascii_art()

    while True:
        try:
            duration = round(float(input("For how many hours do you want to record the temperature?: ")))
            interval = round(float(input("The interval to record temperature in minutes: ")))
            your_city = str(input("Enter you city: ").title())
            break
        except ValueError:
            print("Invalid input.")
        except KeyboardInterrupt:
            exit("exited by user")

    success = record_and_display_temperature(duration, interval, your_city)

    file_path = "temperature_data.txt"
    data = read_temperature_data(file_path)

    if success:
        max_temp, min_temp = display_temperature_data(data)
        print(f"\nMaximum Temperature: {max_temp:.2f} C")
        print(f"Minimum Temperature: {min_temp:.2f} C")
        with open("max_min.txt", "w") as file:
            json.dump({"max_temperature": max_temp, "min_temperature": min_temp}, file)
        print("File max_min has been written.")
    else:
        print("No temperature data available.")

def record_and_display_temperature(duration, interval, your_city):
    api_key = "e159d8b19903e1acaad8c920d3a8ea9e"
    city_name = your_city
    duration_limit_hours = duration
    start_time = time.time()
    temperature_data = []
    success = True

    while time.time() - start_time < duration_limit_hours * 3600:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                weather_data = response.json()
                temperature_celsius = weather_data['main']['temp'] - 273.15
                timestamp = datetime.now()

                temperature_data.append({
                    'timestamp': timestamp.isoformat(),
                    'temperature': temperature_celsius
                    })

                print(f"At {timestamp}: Temperature is {temperature_celsius:.2f} C")

                with open("temperature_data.txt", "w") as file:
                    json.dump(temperature_data, file, cls=DateTimeEncoder)

                    time.sleep(interval * 60)
            except KeyboardInterrupt:
                exit("Exited by user")

        elif response.status_code == 404:
            print(f"City '{your_city}' not found. Plese enter a valid city.")
            success = False
            break

        else:
            print(f"Error: {response.status_code}")
            success = False
            print(response.text)
            break

    print("File temperature_data.txt has been written.")
    return success

def read_temperature_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data_str = file.read()
            temperature_data = json.loads(data_str, object_hook=date_hook)
            return temperature_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def display_temperature_data(temperature_data):
    max_temperature = float('-inf')
    min_temperature = float('inf')

    for entry in temperature_data:
        timestamp = entry['timestamp']
        temperature = entry['temperature']
        print(f"At {timestamp}: Temperature is {temperature:.2f} C")
        max_temperature = max(max_temperature, temperature)
        min_temperature = min(min_temperature, temperature)

    return max_temperature, min_temperature

def date_hook(obj):
    if 'timestamp' in obj:
        obj['timestamp'] = datetime.fromisoformat(obj['timestamp'])
    return obj

def ascii_art():
    custom_fig = Figlet(font='slant')
    ascii_art = custom_fig.renderText("Temperature Recorder")
    print(ascii_art)

if __name__ == "__main__":
    main()

