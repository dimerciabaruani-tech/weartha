# weather_utils.py
import requests
from datetime import datetime

def get_weather_by_city(city: str, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_weather_by_coords(lat: float, lon: float, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_forecast_by_city(city: str, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_forecast_by_coords(lat: float, lon: float, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def parse_forecast_data(forecast_json):
    daily_data = {}
    for entry in forecast_json['list']:
        date_obj = datetime.fromtimestamp(entry['dt'])
        day_key = date_obj.strftime('%Y-%m-%d')
        day_label = date_obj.strftime('%a %d') # e.g., Mon 14
        
        if day_key not in daily_data:
            daily_data[day_key] = {
                'label': day_label,
                'max_temp': -100, 'min_temp': 100,
                'icon': entry['weather'][0]['icon']
            }
        temp = entry['main']['temp']
        daily_data[day_key]['max_temp'] = max(daily_data[day_key]['max_temp'], temp)
        daily_data[day_key]['min_temp'] = min(daily_data[day_key]['min_temp'], temp)

    sorted_days = sorted(daily_data.items())[:7]
    today = datetime.now().date()
    
    result = []
    for i, (k, v) in enumerate(sorted_days):
        date_obj = datetime.strptime(k, '%Y-%m-%d').date()
        if i == 0:
            label = "Today"
        elif i == 1:
            label = "Tomorrow"
        else:
            label = date_obj.strftime('%a')
        result.append({
            'date': date_obj.strftime('%d/%m'),
            'label': label,
            'max': v['max_temp'],
            'min': v['min_temp'],
            'icon': v['icon']
        })
    return result

def parse_hourly_data(forecast_json, limit=8):
    hourly = []
    for entry in forecast_json['list'][:limit]:
        dt = datetime.fromtimestamp(entry['dt'])
        hourly.append({
            'time': dt.strftime('%H:%M'),
            'temp': entry['main']['temp'],
            'icon': entry['weather'][0]['icon']
        })
    return hourly

def get_time_of_day_greeting():
    now = datetime.now()
    hour = now.hour
    if hour < 12: return {"text": "Good morning", "period": "morning"}
    elif hour < 18: return {"text": "Good afternoon", "period": "afternoon"}
    elif hour < 21: return {"text": "Good evening", "period": "evening"}
    else: return {"text": "Good night", "period": "night"}