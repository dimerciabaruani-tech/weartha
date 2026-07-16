# weather_utils.py
import requests
from datetime import datetime, timedelta

def get_current_weather(city: str, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_forecast(city: str, api_key: str, units: str):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": units}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def parse_forecast_data(forecast_json, unit_symbol):
    """Organizes 5-day/3-hour forecast into a daily summary structure"""
    daily_data = {}
    
    for entry in forecast_json['list']:
        date_obj = datetime.fromtimestamp(entry['dt'])
        day_key = date_obj.strftime('%Y-%m-%d')
        date_str = date_obj.strftime('%a %d') # e.g., Mon 14
        
        if day_key not in daily_data:
            daily_data[day_key] = {
                'date': date_str,
                'temps': [],
                'condition': entry['weather'][0]['main'],
                'icon': entry['weather'][0]['icon'],
                'max_temp': -100,
                'min_temp': 100
            }
        
        temp = entry['main']['temp']
        daily_data[day_key]['temps'].append(temp)
        daily_data[day_key]['max_temp'] = max(daily_data[day_key]['max_temp'], temp)
        daily_data[day_key]['min_temp'] = min(daily_data[day_key]['min_temp'], temp)

    # Sort and limit to 7 days
    sorted_days = sorted(daily_data.items())[:7]
    return [{'day': v['date'], 'max': v['max_temp'], 'min': v['min_temp'], 
             'condition': v['condition']} for k, v in sorted_days]

def get_time_of_day_greeting():
    """Returns a dict with greeting text and a 'period' key so the UI can
    pair it with a proper line-icon instead of an emoji glyph."""
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        return {"text": "Good morning", "period": "morning"}
    elif hour < 18:
        return {"text": "Good afternoon", "period": "afternoon"}
    elif hour < 21:
        return {"text": "Good evening", "period": "evening"}
    else:
        return {"text": "Good night", "period": "night"}