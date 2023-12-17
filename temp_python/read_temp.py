# read_temp
import json
from datetime import datetime

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
        print(f"At {timestamp}: Temperature is {temperature:.2f} °C")

        # Update max and min temperatures
        max_temperature = max(max_temperature, temperature)
        min_temperature = min(min_temperature, temperature)

    return max_temperature, min_temperature

def date_hook(obj):
    if 'timestamp' in obj:
        obj['timestamp'] = datetime.fromisoformat(obj['timestamp'])
    return obj

if __name__ == "__main__":
    file_path = "temperature_data.txt"
    data = read_temperature_data(file_path)

    if data:
        max_temp, min_temp = display_temperature_data(data)
        print(f"\nMaximum Temperature: {max_temp:.2f} °C")
        print(f"Minimum Temperature: {min_temp:.2f} °C")
        with open("max_min.txt", "w") as file:
            json.dump({"max_temperature": max_temp, "min_temperature": min_temp}, file)
        print("File max_min.txt has been written.")
    else:
        print("No temperature data available.")
