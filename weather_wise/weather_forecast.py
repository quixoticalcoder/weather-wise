import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import pytz
from datetime import datetime

api_key = os.environ.get("OPENWEATHER_API_KEY", "")
api_endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
units = 'metric'

def utc_to_ist(utc_time):
    utc = pytz.utc.localize(utc_time)
    ist = utc.astimezone(pytz.timezone('Asia/Kolkata'))
    return ist

def fetch_weather():
    city_name = city_entry.get().strip()
    if not city_name:
        messagebox.showerror("Error", "Enter a city name.")
        return
    if not api_key:
        messagebox.showerror("Error", "Set OPENWEATHER_API_KEY before starting weather-wise.")
        return
    query_params = {'q': city_name, 'appid': api_key, 'units': units}

    try:
        response = requests.get(api_endpoint, params=query_params, timeout=15)
    except requests.RequestException:
        messagebox.showerror("Error", "Unable to fetch weather. Check your connection and try again.")
        return
    
    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']

        forecast_text.delete('1.0', tk.END)  # Clear previous forecast

        for forecast in forecast_list:
            utc_timestamp = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            ist_timestamp = utc_to_ist(utc_timestamp)
            
            temperature = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            
            forecast_text.insert(tk.END, f"Time: {ist_timestamp.strftime('%Y-%m-%d %I:%M %p')}\n")
            forecast_text.insert(tk.END, f"Temperature: {temperature}°C\n")
            forecast_text.insert(tk.END, f"Humidity: {humidity}%\n")
            forecast_text.insert(tk.END, "-------------------------\n")

    else:
        error_message = f'Error: {response.status_code} - {response.text}'
        messagebox.showerror("Error", error_message)
#GUI
root = tk.Tk()
root.title("weather-wise")

style = ThemedStyle(root)
style.set_theme("elegance")  

city_label = ttk.Label(root, text="Enter city name:")
city_label.pack(pady=10)

city_entry = ttk.Entry(root)
city_entry.pack(pady=5)

fetch_button = ttk.Button(root, text="Fetch Weather", command=fetch_weather)
fetch_button.pack(pady=5)

forecast_text = tk.Text(root, height=15, width=50)
forecast_text.pack(padx=10, pady=10)

root.mainloop()




