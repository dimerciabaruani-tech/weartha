# app.py
import streamlit as st
import requests
from weather_utils import (
    get_weather_by_city, get_weather_by_coords,
    get_forecast_by_city, get_forecast_by_coords,
    parse_forecast_data, parse_hourly_data, get_time_of_day_greeting
)
from clothing_engine import get_recommendation_from_prefs
from ui_components import load_css, display_outfit_recommendation, get_icon_svg

st.set_page_config(page_title="Wearther", page_icon="🌤", layout="centered")
load_css()

# --- Helpers for dynamic background ---
def get_sky_gradient(condition, period):
    condition = condition.lower()
    if "night" in period or "evening" in period:
        return "#0f172a", "#1e293b" # Night blues
    if "rain" in condition or "thunderstorm" in condition:
        return "#475569", "#334155" # Rainy greys
    if "cloud" in condition or "mist" in condition or "fog" in condition:
        return "#64748b", "#475569" # Cloudy
    return "#38bdf8", "#7dd3fc" # Clear Sky (Bright blue)

# --- Geolocation & State Initialization ---
if 'city' not in st.session_state:
    st.session_state.city = ""
if 'auto_loaded' not in st.session_state:
    st.session_state.auto_loaded = False

# --- Sidebar for Prefs ---
with st.sidebar:
    st.markdown(f'{get_icon_svg("gear", color="#8B93A6", size=15)} Personalize', unsafe_allow_html=True)
    temp_pref = st.selectbox(
        "Temperature Sensitivity",
        ["I'm pretty neutral", "I get cold easily", "I get hot easily"],
        label_visibility="collapsed"
    )
    st.caption("Adjusts recommendations based on how you feel.")

# --- Header (City Management) ---
st.markdown("""
<div class="top-nav">
    <span class="icon-btn">←</span>
    <span>City management</span>
    <span class="icon-btn">+</span>
</div>
""", unsafe_allow_html=True)

# --- Location Input and Auto-Detect ---
location_col1, location_col2 = st.columns([3, 1])
with location_col1:
    city_input = st.text_input("Location", placeholder="e.g. Cape Town or allow GPS below", label_visibility="collapsed")
with location_col2:
    loc_toggle = st.toggle("Auto", value=True, help="Attempt auto-location via GPS/IP")

# Native Browser Geolocation (Streamlit 1.34+)
geo_data = st.geolocation_toggle()
location_coords = None
if geo_data:
    if geo_data.get('latitude') and geo_data.get('longitude'):
        location_coords = (geo_data['latitude'], geo_data['longitude'])

# Auto-detection logic
if loc_toggle and not st.session_state.auto_loaded:
    if location_coords:
        st.session_state.city = "GPS Detected" # placeholder
        st.session_state.lat = location_coords[0]
        st.session_state.lon = location_coords[1]
        st.session_state.auto_loaded = True
        st.rerun()
    elif not city_input:
        try:
            ip_response = requests.get('https://ipapi.co/json/', timeout=5)
            if ip_response.status_code == 200:
                ip_data = ip_response.json()
                auto_city = ip_data.get('city', '')
                if auto_city:
                    st.session_state.city = auto_city
                    st.session_state.auto_loaded = True
                    st.rerun()
        except:
            pass

if city_input:
    st.session_state.city = city_input
    st.session_state.auto_loaded = True

# --- API Key ---
api_key = st.secrets.get("OWM_API_KEY", "") if hasattr(st, "secrets") else ""
if not api_key:
    api_key = st.text_input("OpenWeatherMap API key", type="password", label_visibility="collapsed")

# --- Main Logic ---
if st.session_state.city or location_coords:
    unit_param = "metric"
    
    try:
        # Determine weather fetch method
        if hasattr(st.session_state, 'lat') and hasattr(st.session_state, 'lon') and st.session_state.lat:
            weather_data = get_weather_by_coords(st.session_state.lat, st.session_state.lon, api_key, unit_param)
            forecast_data = get_forecast_by_coords(st.session_state.lat, st.session_state.lon, api_key, unit_param)
            city_name = weather_data.get('name', 'Your Location')
        else:
            weather_data = get_weather_by_city(st.session_state.city, api_key, unit_param)
            forecast_data = get_forecast_by_city(st.session_state.city, api_key, unit_param)
            city_name = weather_data['name']

        # Extract data
        temp = weather_data['main']['temp']
        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        country = weather_data['sys']['country']

        # --- Dynamic Sky Background ---
        greeting = get_time_of_day_greeting()
        top, bottom = get_sky_gradient(condition, greeting['period'])
        st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(180deg, {top} 0%, {bottom} 100%) !important;
            }}
        </style>
        """, unsafe_allow_html=True)

        # --- 1. Main Weather Card ---
        st.markdown(f"""
        <div class="glass-card weather-main">
            <div class="loc">{city_name}, {country}</div>
            <div class="temp">{temp:.0f}°</div>
            <div class="condition">{description.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)

        # --- 2. Hourly Forecast ---
        hourly_data = parse_hourly_data(forecast_data, limit=8)
        hourly_html = '<div class="hourly-scroll">'
        for h in hourly_data:
            hourly_html += f"""
            <div class="hourly-item">
                <span class="h-time">{h['time']}</span>
                <img src="https://openweathermap.org/img/wn/{h['icon']}@2x.png" alt="icon">
                <span class="h-temp">{h['temp']:.0f}°</span>
            </div>
            """
        hourly_html += '</div>'
        st.markdown(f'<div class="glass-card">{hourly_html}</div>', unsafe_allow_html=True)

        # --- 3. Daily Forecast (Vertical List) ---
        daily_data = parse_forecast_data(forecast_data)
        daily_html = '<div class="daily-list">'
        for d in daily_data:
            daily_html += f"""
            <div class="row">
                <div class="day-col">
                    <span class="day-date">{d['date']}</span>
                    <span class="day-label">{d['label']}</span>
                </div>
                <img class="day-icon" src="https://openweathermap.org/img/wn/{d['icon']}@2x.png" alt="icon">
                <div class="day-temps">
                    <span>{d['max']:.0f}°</span>
                    <span class="day-min">{d['min']:.0f}°</span>
                </div>
            </div>
            """
        daily_html += '</div>'
        st.markdown(f'<div class="glass-card">{daily_html}</div>', unsafe_allow_html=True)

        # --- 4. Details Grid ---
        st.markdown(f"""
        <div class="glass-card">
            <div class="detail-grid">
                <div class="detail-item">
                    <div class="val">{feels_like:.0f}°</div>
                    <div class="lbl">Feels like</div>
                </div>
                <div class="detail-item">
                    <div class="val">{humidity}%</div>
                    <div class="lbl">Humidity</div>
                </div>
                <div class="detail-item">
                    <div class="val">{wind_speed:.1f} m/s</div>
                    <div class="lbl">Wind</div>
                </div>
                <div class="detail-item">
                    <div class="val">{pressure} hPa</div>
                    <div class="lbl">Pressure</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- 5. Outfit Recommendation ---
        items = get_recommendation_from_prefs(
            temp_c=temp,
            condition=condition,
            wind_speed=wind_speed,
            humidity=humidity,
            uv_index=0, # API extended key required for UV
            user_prefs=temp_pref
        )
        st.markdown(f'<div class="section-label">{get_icon_svg("hanger")} Complete Outfit</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card">{display_outfit_recommendation(items)}</div>', unsafe_allow_html=True)

    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: Check your API key or city name. {e}")
    except Exception as e:
        st.error(f"System Error: {e}")

else:
    st.info("Enter a city or enable auto-location (GPS/IP) to get personalized outfit recommendations based on your local weather!")